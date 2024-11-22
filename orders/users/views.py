import email
from django.shortcuts import render
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
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
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.core.exceptions import ValidationError



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
    


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]  # Доступно всем

    def post(self, request):
        username = request.data.get('username')

        if not username:
            return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Генерация токена для сброса пароля
        token = default_token_generator.make_token(user)
        reset_url = f'{settings.FRONTEND_URL}/api/users/password-reset/confirm/?token={token}&username={user.username}'

        # Отправка email с ссылкой
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_url}',
            '........',  # Замените на ваш email
            [user.email],
            fail_silently=False,
        )

        return Response({'detail': 'Password reset link sent to email.'}, status=status.HTTP_200_OK)
    


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]  # Доступно всем

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        uidb64 = request.data.get('uid')

        # Проверяем наличие обязательных параметров
        if not token or not new_password or not uidb64:
            return Response(
                {'detail': 'Token, new password, and UID are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Декодируем UID и ищем пользователя
            user_id = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(id=user_id)

            # Проверяем токен
            if not default_token_generator.check_token(user, token):
                return Response(
                    {'detail': 'Invalid or expired token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверяем новый пароль
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Устанавливаем новый пароль
            user.set_password(new_password)
            user.save()

            return Response(
                {'detail': 'Password has been reset successfully.'},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )