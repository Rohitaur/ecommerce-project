from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    
    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        serializer.save(
            user=self.request.user,
            amount=order.total_price  # Order model me total_price field hona chahiye
        )