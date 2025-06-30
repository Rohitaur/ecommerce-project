from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied



class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Registration successful",
                "key": "success",
                "status": status.HTTP_201_CREATED,
                "data": {
                    "email": user.email,
                    "name": user.name,
                    "phone": user.phone,
                }
            }, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message = " | ".join(error_messages) if error_messages else "Registration failed"
            return Response({
                "message": error_message,
                "key": "error",
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            user_data = {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
            return Response({
                "message": "Login successful",
                "key": "success",
                "status": status.HTTP_200_OK,
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data
                }
            }, status=status.HTTP_200_OK)
        else:
            # Collect error messages from serializer.errors
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message = " | ".join(error_messages) if error_messages else "Login failed"
            return Response({
                "message": error_message,
                "key": "error",
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserListAPI(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        # Admin/superuser can access anyone, normal user only self
        if user.is_superuser or user.is_staff:
            return obj
        if obj.id != user.id:
            raise PermissionDenied("You do not have permission to access this user.")
        return obj