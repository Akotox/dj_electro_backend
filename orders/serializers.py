from rest_framework import serializers

from address.serializers import AddressSerializer
from orders.models import OrderItem, Order
from stores.models import StoreOrder
from stores.serializers import StoreBasicSerializer
from products.serializers import ProductPartialSerializer, VariationSerializer, AccessorySerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_data = ProductPartialSerializer(source='product', read_only=True)
    store_data = StoreBasicSerializer(source='store', read_only=True)
    variation_data = VariationSerializer(source='variation_ref', read_only=True)
    accessory_data = AccessorySerializer(source='accessory_ref', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product','reference', 'user_id', 'store', 'quantity', 'price',
            'variation_ref', 'accessory_ref', 'color',
            'product_data', 'store_data', 'variation_data', 'accessory_data'
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    store = StoreBasicSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'store', 'order_items', 'total_price', 'order_status',
            'created_at', 'updated_at', 'delivery_price', 'payment_method',
            'payment_status', 'address', 'rated_products'
        ]


class StoreOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # Nested OrderItem serializer
    address = AddressSerializer(read_only=True)  # Nested Address serializer

    class Meta:
        model = StoreOrder
        fields = ['id', 'store_reference', 'order_reference', 'order_items', 'address', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']