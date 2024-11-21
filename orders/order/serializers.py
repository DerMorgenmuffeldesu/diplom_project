from rest_framework import serializers
from .models import Order, OrderProduct

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='orderproduct_set')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'status', 'total_price', 'order_products']

        def create(self, validated_data):
            order_products_data = validated_data.pop('order_products')
            order = Order.objects.create(**validated_data)
            for item_data in order_products_data:
                product = item_data['product']
                quantity = item_data['quantity']
                total_price = product.price * quantity
                OrderProduct.objects.create(order=order, product=product, quantity=quantity, total_price=total_price)
            order.update_total_price()
            return order
