from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from products.models import Supplier
from users.models import ShippingAddress


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_quantity(self):
        # Считаем общее количество товаров в заказе
        return sum(order_product.quantity for order_product in self.orderproduct_set.all())
    
    def get_total_amount(self):
        total = sum(order_product.product.price * order_product.quantity for order_product in self.orderproduct_set.all())
        return f"{total:,.2f} руб." #форматирование строки в валюте
    
    def update_total_amount(self):
        total = sum(order_product.product.price * order_product.quantity for order_product in self.orderproduct_set.all())
        self.total_amount = total
        self.save()



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True, null=True)
    specification = models.JSONField(blank=True, null=True)  # Если есть спецификация товара
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total_price()


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name