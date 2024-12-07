from django.shortcuts import render, redirect
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import serialize
from .serializers import RegisterSerializer, LoginSerializer, ShippingAddressSerializer, SomeSerializer, PasswordResetSerializer
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
import requests



class RegisterView(APIView):
    """
        Регистрация пользователя

    """
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации
    queryset = User.objects.all()
    serializer_class = RegisterSerializer 
    authentication_classes = [] 


    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Сохраняем пользователя
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginView(APIView):
    """
        Авторизация пользователя

    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

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
    

class YandexOAuthRedirectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        yandex_oauth_url = (
            "https://oauth.yandex.ru/authorize?"
            "response_type=code&"  # Меняем на получение code
            "client_id=your client id"
        )
        return redirect(yandex_oauth_url)



class YandexOAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')  # Получаем code из URL
        if not code:
            return Response({'error': 'Authorization code is missing'}, status=400)

        # Обмениваем code на access_token
        response = requests.post(
            'https://oauth.yandex.ru/token',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': 'your client id',
                'client_secret': 'your client secret',  
            }
        )

        token_data = response.json()
        if 'access_token' not in token_data:
            return Response({'error': 'Failed to obtain access token'}, status=400)

        # Делаем запрос к Yandex API с токеном
        user_response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {token_data["access_token"]}'}
        )
        user_info = user_response.json()

        if 'login' not in user_info:
            return Response({'error': 'Failed to verify token'}, status=400)

        return Response({'user_info': user_info})


class ProtectedView(APIView):
    serializer_class = SomeSerializer 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Отправляем данные о пользователе
        serializer = self.get_serializer({
            'user_id': request.user.id,
            'username': request.user.username,
            'email': request.user.email
        })
        return Response(serializer.data)
    


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]  # Доступно только аутентифицированным пользователям
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = request.user

            # Проверяем старый пароль
            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=400)

            # Устанавливаем новый пароль
            user.set_password(new_password)
            user.save()

            return Response({'detail': 'Password has been successfully updated.'}, status=200)
        return Response(serializer.errors, status=400)



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