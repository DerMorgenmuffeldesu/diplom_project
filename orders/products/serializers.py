from rest_framework import serializers
from .models import Supplier, Product, ProductAttribute, Specification



class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'supplier_name', 'email', 'contact_info']


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['spec_name', 'spec_value']


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value']



class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'supplier', 'description', 'price', 'color', 'stock', 'is_available', 'specifications']

    def create(self, validated_data):
        specifications_data = validated_data.pop('specifications', [])
        product = Product.objects.create(**validated_data)

        for spec in specifications_data:
            Specification.objects.create(product=product, **spec)

        return product
    
    def to_representation(self, instance):
        """
        Переопределяем метод для правильного отображения спецификаций.
        """
        representation = super().to_representation(instance)
        representation['specifications'] = SpecificationSerializer(instance.specifications.all(), many=True).data
        return representation
