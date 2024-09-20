from rest_framework import serializers

from products.models import Product, Accessory, Variation, Category, Brand
from stores.models import Store
from stores.serializers import StoreBasicSerializer


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = ['id', 'title', 'reference', 'price', 'image_url']


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['id', 'title', 'color', 'capacity', 'reference', 'price', 'image_url']


class ProductSerializer(serializers.ModelSerializer):
    accessories = AccessorySerializer(many=True, read_only=True)
    variations = VariationSerializer(many=True, read_only=True)
    store_ref = StoreBasicSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'description', 'is_available', 'discount', 'is_featured', 'product_type',
            'condition', 'ratings', 'rating_count', 'reviews', 'color', 'image_urls',
            'capacity', 'category', 'brand', 'accessories', 'variations', 'store_ref'
        ]

class AddProductSerializer(serializers.ModelSerializer):
    accessories = AccessorySerializer(many=True, read_only=True)
    variations = VariationSerializer(many=True, read_only=True)
    store_ref = StoreBasicSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'description', 'is_available','discount', 'is_featured', 'product_type',
            'condition', 'ratings', 'rating_count', 'reviews', 'color', 'image_urls',
            'capacity', 'category', 'brand', 'accessories', 'variations', 'store_ref'
        ]

    def validate_store_ref(self, value):
        try:
            store = Store.objects.get(id=value)
        except Store.DoesNotExist:
            raise serializers.ValidationError("Store reference does not exist")
        return store

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'id', 'imageUrl']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title', 'id', 'imageUrl']


class ProductPartialSerializer(serializers.ModelSerializer):
    product_image = serializers.URLField(source='image_urls[0]', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'product_image']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'is_available','discount', 'product_type',
            'condition', 'ratings', 'rating_count', 'image_urls',
            'capacity', 'category', 'brand',
        ]
