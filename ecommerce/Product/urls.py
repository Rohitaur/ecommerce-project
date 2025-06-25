from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet , ProductImageViewSet, ProductVariantViewSet, ProductReviewViewSet

router = DefaultRouter()
router.register(r'images', ProductImageViewSet, basename='productimages')
router.register(r'variants', ProductVariantViewSet, basename='productvariants')
router.register(r'reviews', ProductReviewViewSet, basename='productreviews')
router.register(r'', ProductViewSet, basename='product')



urlpatterns = [
    path('', include(router.urls)),
]