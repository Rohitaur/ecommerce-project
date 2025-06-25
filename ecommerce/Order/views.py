from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order
from .serializers import OrderSerializer, DeliveryStatusSerializer, CancelOrderSerializer
from Payment.models import Payment

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='place-order')
    def place_order(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            # Payment create karo
            Payment.objects.create(
                order=order,
                user=request.user,
                amount=order.total_price,  # Order model me total_price hona chahiye
                payment_method='cod'
            )
            order.refresh_from_db()  # Fresh order fetch for response
            response_serializer = OrderSerializer(order)
            return Response({
                "message": "Order placed successfully",
                "key": "success",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Order placement failed",
            "key": "error",
            "status": status.HTTP_400_BAD_REQUEST,
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='my-orders')
    def user_orders(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "message": "User orders fetched successfully",
            "key": "success",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='admin-orders', permission_classes=[IsAdminUser])
    def admin_orders(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "message": "All orders fetched successfully",
            "key": "success",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update-delivery-status', permission_classes=[IsAdminUser])
    def update_delivery_status(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({
                "message": "Order not found.",
                "key": "error",
                "status": status.HTTP_404_NOT_FOUND,
                "data": {}
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = DeliveryStatusSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Payment status update
            if hasattr(order, 'payment'):
                if serializer.validated_data.get('order_status') == 'delivered':
                    order.payment.is_paid = True
                else:
                    order.payment.is_paid = False
                order.payment.save()
                # Payment status update
                order.payment.refresh_from_db()
            # Fresh order fetch for response
            order.refresh_from_db()
            response_serializer = OrderSerializer(order)
            return Response({
                "message": "Order status updated successfully",
                "key": "success",
                "status": status.HTTP_200_OK,
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Order status update failed",
            "key": "error",
            "status": status.HTTP_400_BAD_REQUEST,
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff and order.user != request.user:
            return Response({"detail": "You are not allowed to cancel this order."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CancelOrderSerializer(data=request.data)
        if serializer.is_valid():
            reason = serializer.validated_data.get('reason')
            print(f"Order {pk} cancelled by {request.user.name} for reason: {reason}")
            order.order_status = 'cancelled'
            order.save()
            # Payment status update
            if hasattr(order, 'payment'):
                order.payment.is_paid = False
                order.payment.save()
            # Fresh order fetch for response
            order.refresh_from_db()
            response_serializer = OrderSerializer(order)
            return Response({
                "message": "Order cancelled successfully.",
                "key": "success",
                "status": status.HTTP_200_OK,
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)