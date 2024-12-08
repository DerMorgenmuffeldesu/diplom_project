from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny



class TestErrorView(APIView):
    """
    Этот эндпоинт используется для тестирования интеграции Rollbar.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        raise Exception("Test exception for Rollbar")  # Искусственно создаем исключение


