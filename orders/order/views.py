from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Order, OrderProduct
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product, Supplier, Specification
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from users.serializers import ShippingAddressSerializer
from users.models import ShippingAddress



class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        orders_data = request.data if isinstance(request.data, list) else [request.data]
        created_orders = []

        for order_data in orders_data:
            items_data = order_data.get('items', [])
            if not items_data:
                return Response({"error": "Each order must have at least one item."}, status=status.HTTP_400_BAD_REQUEST)

            customer_id = order_data.get('customer')
            try:
                customer = User.objects.get(id=customer_id)
            except User.DoesNotExist:
                return Response({"error": f"User with ID {customer_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)


            # Получаем  адрес доставки, если он есть
            shipping_address_data = order_data.get('shipping_address', None)
            shipping_address = None


            # Проверяем, если есть shipping_address в запросе
            if shipping_address_data:
                shipping_address_serializer = ShippingAddressSerializer(data=shipping_address_data)
                if shipping_address_serializer.is_valid():
                    shipping_address = shipping_address_serializer.save(user=customer)
                else:
                    return Response(shipping_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

            # Создаем заказ
            order = Order.objects.create(customer=customer, shipping_address=shipping_address)

        # Добавляем товары в заказ
            for item in items_data:
                name = item.get('name')
                supplier_id = item.get('supplier_id')
                quantity = item.get('quantity', 1)
                specification = item.get('specification', [])

                try:
                    product = Product.objects.get(name=name)
                except Product.DoesNotExist:
                    return Response({"error": f"Product with name {name} does not exist."}, status=status.HTTP_404_NOT_FOUND)

                try:
                    supplier = Supplier.objects.get(id=supplier_id)
                except Supplier.DoesNotExist:
                    return Response({"error": f"Supplier with ID {supplier_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

                # Добавление товара в заказ
                OrderProduct.objects.create(
                    order=order, product=product, supplier=supplier, quantity=quantity,
                    color=product.color, specification=specification, shipping_address=shipping_address
                )

            created_orders.append(order)

        # Отправляем результат
        serializer = self.get_serializer(created_orders, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


