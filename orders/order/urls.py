from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from django.urls import path, include
from users.views import ShippingAddressViewSet

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'shipping-addresses', ShippingAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),  # подключение маршрутов из роутера

]