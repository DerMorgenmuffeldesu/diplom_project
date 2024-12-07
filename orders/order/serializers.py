from rest_framework import serializers
from .models import Order, OrderProduct
from products.serializers import ProductSerializer, SupplierSerializer
from users.serializers import ShippingAddressSerializer
from users.models import ShippingAddress



class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'supplier', 'color', 'specification']



class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproduct_set', many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(required=False)

    class Meta:
        model = Order
        fields = ['id', 'products', 'customer', 'created_at', 'status', 'shipping_address', 'total_amount', 'total_amount']

    def create(self, validated_data):
        shipping_address_data = validated_data.pop('shipping_address', None)

        order = Order.objects.create(**validated_data)
        
        if shipping_address_data:
            # Создаем новый адрес, если передан
            shipping_address = ShippingAddress.objects.create(**shipping_address_data)
            order.shipping_address = shipping_address
            order.save()
     
        return order
    