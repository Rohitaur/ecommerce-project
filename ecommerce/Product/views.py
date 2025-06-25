from rest_framework import viewsets, status, filters , permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product, ProductImage , ProductVariant, ProductReview
from .serializers import ProductSerializer , ProductImageSerializer, ProductVariantSerializer, ProductReviewSerializer
from Order.models import Order



class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can add/delete images



class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can add/update/delete   


class ProductFilter(FilterSet):
    price_min = NumberFilter(field_name="price", lookup_expr='gte')
    price_max = NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'name', 'price_min', 'price_max']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    filterset_fields = ['category', 'price', 'brand', 'name']
    search_fields = ['name', 'brand']
    ordering_fields = ['name', 'price', 'created_at', 'brand']  
    def get_permissions(self):
        """
        Modify permissions based on action:
        - Admin can create, update, delete
        - Any authenticated user can retrieve (view) products
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Only admins can create, update, or destroy
        return super().get_permissions()  # Allow authenticated users to view details

    # POST
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Product created successfully",
                "key": "success",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # Collect error messages from serializer.errors
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_messages = " | ".join(error_messages) if error_messages else "Product creation failed"
            return Response({
                "message": "Product creation failed",
                "key": "error",
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

    # GET
    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # PUT: Full update 
    def update(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETE
    def destroy(self, request, pk=None):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    






#reviews


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User apne reviews dekh sakta hai, ya sabhi (agar chaho to filter laga sakte ho)
        return ProductReview.objects.all()

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        user = self.request.user
        # Check: Kya user ne is product ka order kiya hai?
        has_ordered = Order.objects.filter(user=user, product=product, order_status='delivered').exists()
        if not has_ordered:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You can only review products you have purchased and received (delivered).")
        serializer.save(user=user)