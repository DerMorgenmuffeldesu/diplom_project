from rest_framework import serializers
from .models import Order, OrderProduct

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='orderproduct_set')

    class Meta:
        model = Order
        fields = '__all__'
