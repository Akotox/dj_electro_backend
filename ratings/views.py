from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from orders.models import Order
from .models import Rating, Product, Store
from .serializers import RatingSerializer


class AddRatingView(APIView):
    def post(self, request):
        # Extract data from request
        user_id = request.data.get('userId')
        product_id = request.data.get('product_reference')
        store_id = request.data.get('store_reference')
        order_id = request.data.get('order_reference')

        # Ensure the order exists
        try:
            order = Order.objects.get(id=order_id, user=user_id)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the store exists
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"message": "Store not found or is closed"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate and create the rating
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.save()

            # Update rated_products list in the order
            if product_id not in order.rated_products:
                order.rated_products.append(product_id)
                order.save()

            # Update product ratings and rating count
            product_ratings = Rating.objects.filter(product_reference=product)
            product.rating_count = product_ratings.count()
            product.ratings = product_ratings.aggregate(Avg('product_rating'))['product_rating__avg']

            # Get the 3 latest reviews for the product
            latest_reviews = product_ratings.order_by('-created_at')[:3]
            # Extract review text
            product.reviews = latest_reviews

            product.save()

            # Update store rating
            store_ratings = Rating.objects.filter(store_reference=store)
            store.store_rating = store_ratings.aggregate(Avg('store_rating'))['store_rating__avg']
            store.save()

            return Response({"message": "Rating added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingsPagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional, if you want to limit the maximum page size


class UserReviewsList(generics.ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingsPagination

    def get_queryset(self):
        # Get the category_id from query params
        user_id = self.request.query_params.get('user_id')

        # Ensure the category_id is provided
        if not user_id:
            return Response({"message": "User id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter products by the given category ID
        queryset = Rating.objects.filter(user_id=user_id)
        return queryset


class StoreReviewsList(generics.ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingsPagination

    def get_queryset(self):
        # Get the category_id from query params
        store_id = self.request.query_params.get('store_id')

        # Ensure the category_id is provided
        if not store_id:
            return Response({"message": "Store id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter products by the given category ID
        queryset = Rating.objects.filter(store_reference=store_id)
        return queryset


class ProductReviewsList(generics.ListAPIView):
    serializer_class = RatingSerializer
    pagination_class = RatingsPagination

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')

        if not product_id:
            return Response({"message": "Product id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter products by the given category ID
        queryset = Rating.objects.filter(product_reference=product_id)
        return queryset
