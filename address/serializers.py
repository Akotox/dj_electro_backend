from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'phone_number', 'address', 'city', 'user', 'contact_name', 'tag', 'is_default']
