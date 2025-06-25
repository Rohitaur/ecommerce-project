from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'address_line', 'city', 'state', 'postal_code', 'country', 'is_default']
        read_only_fields = ['user']