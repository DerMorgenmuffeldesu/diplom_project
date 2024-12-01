from ast import parse
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
    


    @action(detail=False, methods=['get'], url_path='import-products', url_name='import_products')
    def import_products(self, request, *args, **kwargs):
        user = request.user  # Получаем текущего пользователя из запроса
        orders = Order.objects.filter(customer=user)  # Фильтруем заказы по пользователю

        products = []
        for order in orders:
            for item in order.orderproduct_set.all():
                products.append({
                    "product_id": item.product.id,
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "supplier": item.supplier.supplier_name,
                    "specifications": item.specification,
                })

        return Response({"products": products}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['delete'], url_path='remove-product', url_name='remove_product')
    def remove_product(self, request, pk=None):

        """
        Удаляет товар из заказа (корзины) по ID заказа и ID товара.
        """

        try:
            order = self.get_object()  # Получаем текущий заказ
            product_id = request.data.get('product_id')  # Получаем ID товара из тела запроса

            if not product_id:
                return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Находим товар в заказе
            order_product = order.orderproduct_set.filter(product_id=product_id).first()

            if not order_product:
                return Response({"error": "Product not found in this order."}, status=status.HTTP_404_NOT_FOUND)

            # Удаляем товар
            order_product.delete()
            return Response({"message": "Product removed from order."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['delete'], url_path='remove-shipping-address', url_name='remove_shipping_address')
    def delete_shipping_address(self, request, pk=None):

        """
        Удаляет адрес доставки для указанного заказа.
        
        """
        try:
            order = self.get_object()  # Получаем заказ по ID
            if not order.shipping_address:
                return Response({"error": "This order has no shipping address."}, status=status.HTTP_404_NOT_FOUND)

            # Удаляем адрес доставки
            order.shipping_address.delete()
            order.shipping_address = None
            order.save()

            return Response({"message": "Shipping address removed successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)