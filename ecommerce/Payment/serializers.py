from rest_framework import serializers
from .models import Payment
from Order.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'user', 'amount', 'payment_method', 'is_paid', 'created_at']
        read_only_fields = ['user', 'created_at', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'