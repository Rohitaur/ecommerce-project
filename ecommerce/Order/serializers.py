from rest_framework import serializers
from .models import Order
from Payment.serializers import PaymentSerializer


class OrderSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='product.subcategory.name', read_only=True)
    payment = PaymentSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'subcategory_name','order_status', 'created_at', 'updated_at',  'total_price']

    def create(self, validated_data):
        # subcategory ko product ke through set karo
        product = validated_data['product']
        quantity = validated_data['quantity']

        if product.stock < quantity:
            raise ValidationError("Not enough stock available.")
        
        product.stock -= quantity
        product.save()

        
        validated_data['subcategory'] = product.subcategory
        # user ko bhi set karo agar zarurat ho
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status']


class CancelOrderSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255)