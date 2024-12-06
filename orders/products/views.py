from turtle import color
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Supplier, Product, Specification
from .serializers import SupplierSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import ValidationError



class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('supplier').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    
    def create(self, request, *args, **kwargs):
        """
        Создаёт товар, связанный с существующим поставщиком.
        """
        supplier_name = request.data.get('supplier_name')
        product_data = request.data
        color = product_data.get('color')
        specifications = request.data.pop('specifications', [])

        if not supplier_name:
            return Response(
                {"error": "Пожалуйста, укажите название поставщика."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            supplier = Supplier.objects.get(supplier_name=supplier_name)
        except Supplier.DoesNotExist:
            return Response(
                {"error": f"Поставщик с названием '{supplier_name}' не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.create(
            name=product_data['name'],
            supplier=supplier,
            description=product_data.get('description', ''),
            price=product_data['price'],
            color=color,
            stock=product_data.get('stock', 0),
            is_available=product_data.get('is_available', True),
        )

        # Добавляем спецификации к продукту
        for spec in specifications:
            spec_name = spec.get('spec_name')  # Получаем spec_name из текущего словаря
            spec_value = spec.get('spec_value')  # Получаем spec_value из текущего словаря

            if not spec_name or not spec_value:
                raise ValidationError("Каждая спецификация должна содержать 'spec_name' и 'spec_value'.")

            Specification.objects.create(
                product=product,
                spec_name=spec_name,
                spec_value=spec_value
            )

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)




class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  # Мы будем искать продукт по ID
    