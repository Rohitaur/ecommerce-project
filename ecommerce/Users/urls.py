from django.urls import path
from .views import RegisterAPI, LoginAPI, ProfileAPI, UserDetailAPI, UserListAPI 

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='api-register'),
    path('login/', LoginAPI.as_view(), name='api-login'),
    path('profile/', ProfileAPI.as_view(), name='api-profile'),
    path('<int:id>/', UserDetailAPI.as_view()),
    path('users/', UserListAPI.as_view(), name='api-users'),
]
