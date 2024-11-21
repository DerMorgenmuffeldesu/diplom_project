from django.shortcuts import render
from rest_framework import viewsets
from .models import Supplier, Product
from .serializers import SupplierSerializer, ProductSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

