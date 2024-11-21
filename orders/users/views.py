from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User


class RegisterView(APIView):
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
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        user = User.objects.filter(username=username).first()
        
        if user:
            reset_token = user.password_reset_token  # Или используйте стандартный токен Django
            reset_url = f"{settings.FRONTEND_URL}/reset-password/?token={reset_token}"
            
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_url}',
                'no-reply@example.com',
                [user.email],
            )
            return Response({'message': 'Password reset link sent'}, status=200)
        return Response({'error': 'User not found'}, status=404)


