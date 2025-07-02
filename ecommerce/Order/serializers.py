from rest_framework import serializers
from .models import Order
from Payment.serializers import PaymentSerializer
from rest_framework.exceptions import ValidationError
from Product.models import ProductVariant
from Payment.models import Payment
from Address.models import Address


class OrderSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='product.subcategory.name', read_only=True)
    payment = PaymentSerializer(read_only=True)
    address_id = serializers.IntegerField(write_only=True )
    payment_method = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'subcategory_name','order_status', 'created_at', 'updated_at',  'total_price']

    def create(self, validated_data):
        # subcategory ko product ke through set karo
        product = validated_data['product']
        quantity = validated_data['quantity']
        address_id = validated_data.pop('address_id')
        payment_method = validated_data.pop('payment_method')

        variant = ProductVariant.objects.filter(product=product, stock__gte=quantity).first()

        # if variant is None:
        #     raise ValidationError("Product variant is required.")

        # if variant.stock < quantity:
        #     raise ValidationError("Not enough stock available.")

        if not variant:
            raise ValidationError("No variant has enough stock for this product.")

        variant.stock -= quantity
        variant.save()

        
        validated_data['subcategory'] = product.subcategory
        validated_data['variant'] = variant
        # user ko bhi set karo agar zarurat ho
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise ValidationError("User authentication is required.")
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            raise ValidationError("Address not found or does not belong to user.")

        validated_data['address'] = address
            
        order = super().create(validated_data)

        Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_price,
            payment_method=payment_method,
            is_paid=(payment_method != 'cod')  # COD: False, otherwise True
        )

        return order
    
class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status']


class CancelOrderSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255)