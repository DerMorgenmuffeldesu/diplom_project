from django.urls import path
from .views import RegisterView, PasswordResetView, ProtectedView, ShippingAddressViewSet, YandexOAuthRedirectView, YandexOAuthCallbackView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('shipping-addresses/', ShippingAddressViewSet.as_view, name='shipping-addresses'),
    path('api/auth/yandex/start/', YandexOAuthRedirectView.as_view(), name='yandex-oauth-start'),
    path('api/auth/yandex/callback/', YandexOAuthCallbackView.as_view(), name='yandex-oauth-callback'),

]
