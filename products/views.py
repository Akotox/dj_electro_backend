import random

import django_filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from stores.models import Store
from products.models import Category, Brand, Product
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, VariationSerializer, AccessorySerializer


class HomeCategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Get all categories except the "More..." category and annotate with a random value
        queryset = Category.objects.exclude(title="More").annotate(random_order=Count('id'))

        # Shuffle the queryset
        queryset = list(queryset)
        random.shuffle(queryset)

        # Fetch the "More..." category
        more_category = Category.objects.filter(title="More").first()

        # Ensure "More..." is the fifth category if it exists
        if more_category:
            queryset = queryset[:4] + [more_category] + queryset[4:]

        # Return the first 5 categories (with "More..." in the fifth position)
        return queryset[:5]


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    # Exclude categories where title is "More"
    queryset = Category.objects.exclude(title="More")


class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer

    queryset = Brand.objects.all()


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Get only available products and annotate with a random value
        queryset = Product.objects.filter(is_available=True).annotate(random_order=Count('id'))

        # Shuffle the queryset
        queryset = list(queryset)
        random.shuffle(queryset)

        # Return the first 20 products
        return queryset[:20]


class ProductPagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional, if you want to limit the maximum page size


class DiscountedProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        # Get products where discount is greater than 0
        queryset = Product.objects.filter(discount__gt=0)
        return queryset


class CategoryProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        # Get the category_id from query params
        category_id = self.request.query_params.get('category_id')

        # Ensure the category_id is provided
        if not category_id:
            return Response({"error": "Category id provided doesn't match"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter products by the given category ID
        queryset = Product.objects.filter(category__id=category_id)
        return queryset


class BrandProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        # Get the category_id from query params
        brand_id = self.request.query_params.get('brand_id')

        # Ensure the category_id is provided
        if not brand_id:
            return Response({"error": "Brand id provided doesn't match"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter products by the given category ID
        queryset = Product.objects.filter(brand__id=brand_id)
        return queryset


class FilterSimilarProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None  # Disable pagination if you don't need it here

    def get_queryset(self):
        # Get the category from query parameters
        category_id = self.request.query_params.get('category', None)
        product_id = self.request.query_params.get('product_id', None)

        if category_id:
            # Filter products by the given category ID and exclude the current product
            queryset = Product.objects.filter(category_id=category_id)

            if product_id:
                queryset = queryset.exclude(id=product_id)

            # Shuffle the queryset and limit to 6 items
            queryset_list = list(queryset)
            random.shuffle(queryset_list)
            return queryset_list[:6]

        # Return an empty queryset if no category is provided
        return Product.objects.none()


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.NumberFilter(field_name='category', lookup_expr='exact')
    brand = django_filters.NumberFilter(field_name='brand', lookup_expr='exact')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')  # Case-insensitive partial match

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'brand', 'title']


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering = ['-price']  # Default ordering, can be adjusted

    def get(self, request, *args, **kwargs):
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        category = request.query_params.get('category', None)
        brand = request.query_params.get('brand', None)
        title = request.query_params.get('title', None)

        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                if min_price > max_price:
                    return Response({"message": "Minimum price cannot be greater than maximum price."},
                                    status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"message": "Invalid price values provided."}, status=status.HTTP_400_BAD_REQUEST)

        return super().get(request, *args, **kwargs)


class GetProductById(APIView):
    def get(self, request):
        product_id = request.query_params.get('product_id', None)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddVariationToProduct(APIView):
    def post(self, request):
        # Get product ID from the query parameters
        product_id = request.data['reference']

        # Check if the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get variation data from the request
        variation_data = request.data

        # Create and validate the variation
        variation_serializer = VariationSerializer(data=variation_data)
        if variation_serializer.is_valid():
            variation_serializer.save()
            return Response({"message": "Variation added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(variation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAccessoryToProduct(APIView):
    def post(self, request, ):
        product_id = request.data['reference']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        accessory_data = request.data
        accessory_serializer = AccessorySerializer(data=accessory_data)

        if accessory_serializer.is_valid():
            accessory = accessory_serializer.save()
            product.accessories.add(accessory)
            product.save()

            return Response({"message": "Accessory added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(accessory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProduct(APIView):
    def post(self, request):
        product_data = request.data

        # Check if the store reference exists
        store_ref = product_data.get('store_ref')
        try:
            store = Store.objects.get(id=store_ref)
        except Store.DoesNotExist:
            return Response({"message": "Store reference does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # If checks pass, create the product
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product = product_serializer.save()  # Save the product and get the instance
            return Response({"id": product.id}, status=status.HTTP_201_CREATED)  # Return only the id
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckProductAvailability(APIView):
    def get(self, request):
        # Extract the product_id from query parameters
        product_id = request.query_params.get('product_id', None)

        if not product_id:
            return Response({"message": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the product by its ID
            product = Product.objects.get(id=product_id)

            # Return the availability status (true/false)
            return Response({
                "is_available": product.is_available
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            # Return false when the product is not found or unavailable
            return Response({
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)



