from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_DEFAULT, default=None)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(max_length=255, null=True, blank=True)

    def get_default_supplier():
        # Здесь вы можете возвращать конкретного поставщика
        return Supplier.objects.first()  

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_DEFAULT, default=get_default_supplier)

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
