from django.shortcuts import render
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, ShippingAddressSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ValidationError
from .models import ShippingAddress
from rest_framework import viewsets



class RegisterView(APIView):
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации
    authentication_classes = [] 

    def get(self, request):
        return Response({"message": "Register endpoint is active"}, status=200)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access to this resource."})
    


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]  # Доступно только аутентифицированным пользователям

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Проверяем, что оба пароля предоставлены
        if not old_password or not new_password:
            return Response({'detail': 'Both old and new passwords are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Проверяем правильность старого пароля
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка нового пароля (стандартные проверки Django)
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password has been successfully updated.'}, status=status.HTTP_200_OK)



class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Убедимся, что у пользователя не может быть более одного основного адреса
        if serializer.validated_data.get('is_primary', False):
            ShippingAddress.objects.filter(user=self.request.user, is_primary=True).update(is_primary=False)
        
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Не удалять основной адрес доставки, если их больше нет
        if instance.is_primary and ShippingAddress.objects.filter(user=instance.user).count() == 1:
            return Response({"error": "Cannot delete the only primary shipping address."}, status=400)
        instance.delete()