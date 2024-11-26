from django.urls import path, include
from .views import ProductViewSet, SupplierViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Это будет доступно по пути /api/products/
router.register(r'suppliers', SupplierViewSet)  # Это будет доступно по пути /api/suppliers/

urlpatterns = [
    path('', include(router.urls)),  # Это подключает все URL из DefaultRouter
]