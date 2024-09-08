from rest_framework import serializers

from products.models import Product, Accessory, Variation, Category, Brand
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
            'id', 'title', 'price', 'description', 'is_featured', 'product_type',
            'condition', 'ratings', 'rating_count', 'reviews', 'color', 'image_urls',
            'capacity', 'category', 'brand', 'accessories', 'variations', 'store_ref'
        ]


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
