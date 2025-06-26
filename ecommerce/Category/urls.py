from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]




# GET /categories/ — sabhi categories list
# POST /categories/ — nayi category create (admin only)
# GET /categories/<id>/ — ek category detail
# PUT/PATCH /categories/<id>/ — update (admin only)
# DELETE /categories/<id>/ — delete (admin only)