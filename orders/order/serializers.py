from rest_framework import serializers
from .models import Order, OrderProduct
from products.serializers import ProductSerializer, SupplierSerializer



class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'supplier']



class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproduct_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'customer', 'created_at', 'status']
