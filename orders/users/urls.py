from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
]
