from rest_framework import serializers
from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    store_products = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = [
            'id', 'title', 'description', 'address', 'phone_number', 'coverUrl',
            'website', 'logo_url', 'opening_hours', 'store_rating', 'store_products',
            'is_featured', 'created_at', 'updated_at'
        ]

    def get_store_products(self, obj):
        # Import ProductSerializer here to avoid circular import at the top
        from products.serializers import ProductSerializer
        products = obj.product_set.all()  # Assuming reverse relationship from Store to Product
        return ProductSerializer(products, many=True).data


class StoreBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'title', 'logo_url', 'store_rating']
