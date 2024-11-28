from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Order, OrderProduct
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product, Supplier
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Получаем текущего пользователя
        user = request.user

        # Проверяем, есть ли данные для создания заказа
        items_data = request.data.get('items', [])
        if not items_data:
            return Response({"error": "Order must have at least one item."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем заказ
        order = Order.objects.create(customer=user)

        # Добавляем товары в заказ
        for item in items_data:
            product_id = item.get('product_id')
            supplier_id = item.get('supplier_id')
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": f"Product with ID {product_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                return Response({"error": f"Supplier with ID {supplier_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Создаем запись в OrderProduct
            OrderProduct.objects.create(order=order, product=product, supplier=supplier, quantity=quantity)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['get'], parser_classes=[JSONParser])
    def import_user_orders(self, request, *args, **kwargs):
        """
        Возвращает список товаров, которые заказал указанный пользователь.
        """
        # Извлекаем имя пользователя из запроса
        username = request.data.get("username")
        if not username:
            return Response({"error": "Отсутствует имя пользователя."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем существование пользователя
        user = get_object_or_404(User, username=username)

        # Получаем все заказы пользователя
        orders = Order.objects.filter(customer=user)

        # Если заказы отсутствуют
        if not orders.exists():
            return Response({"message": f"У пользователя '{username}' нет заказов."}, status=status.HTTP_200_OK)

        # Сбор информации о товарах
        products = []
        for order in orders:
            order_products = OrderProduct.objects.filter(order=order).select_related('product', 'supplier')
            for op in order_products:
                products.append({
                    "order": order.id,
                    "pname": op.product.name,
                    "name": op.supplier.name,
                    "quantity": op.quantity,
                    "status": order.status,
                    "created_at": order.created_at,
                })

        return Response({"products": products}, status=status.HTTP_200_OK)

