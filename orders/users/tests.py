from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):
    def test_register_user(self):
        """
        Тест регистрации пользователя
        """
        url = reverse('register')  # Убедитесь, что у вас настроен URL с именем 'register'
        data = {'username': 'user1', 'password': 'yathdesu75'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        # Сохраняем пользователя для дальнейшего использования
        self.user = User.objects.get(username='user1')
        print(self.user)

    def test_login_user(self):
        """
        Тест авторизации пользователя
        """
        print(User.objects.all())
        url = reverse('login') 
        data = {'username':'user1', 'password': 'yathdesu75'}  # Используем зарегистрированного пользователя
        response = self.client.post(url, data)

        # Логирование ответа для анализа
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

