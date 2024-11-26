from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Supplier, Product
from .serializers import SupplierSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



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
        name = request.data.get('name')
        product_data = request.data

        if not name:
            return Response(
                {"error": "Пожалуйста, укажите название поставщика."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            supplier = Supplier.objects.get(name=name)
        except Supplier.DoesNotExist:
            return Response(
                {"error": f"Поставщик с названием '{name}' не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.create(
            name=product_data['name'],
            supplier=supplier,
            description=product_data.get('description', ''),
            price=product_data['price'],
            stock=product_data.get('stock', 0),
            is_available=product_data.get('is_available', True)
        )

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)