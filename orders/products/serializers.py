from rest_framework import serializers
from .models import Supplier, Product, ProductAttribute



class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'contact_info']



class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value']



class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'supplier', 'description', 'price', 'stock', 'is_available']
    
