from rest_framework import serializers
from .models import Supplier, Product, ProductAttribute

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['attribute_name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        supplier = validated_data.get('supplier')  # Получаем поставщика из данных
        if not supplier:
            raise serializers.ValidationError("Supplier is required.")
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
