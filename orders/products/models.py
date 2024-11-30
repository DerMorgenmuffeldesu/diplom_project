from django.db import models
from django.contrib.auth.models import User



class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.supplier_name



class Product(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="products")
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    attributes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
  

class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    spec_name = models.CharField(max_length=255)
    spec_value = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.spec_name}: {self.spec_value}"



class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_attributes")
    name = models.CharField(max_length=255)
    value = models.TextField()


    def __str__(self):
        return f"{self.name}: {self.value}"
