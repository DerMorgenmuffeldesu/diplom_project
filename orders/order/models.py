from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # хранит общую сумму заказа

    def update_total_price(self): #пересчитывает общую стоимость заказа, суммируя стоимость всех позиций из связанной модели OrderProduct
        # Суммируем стоимость всех товаров в заказе
        total = sum(item.total_price for item in self.orderproduct_set.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id} by {self.customer}"



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # хранит цену товара, умноженную на количество.

    # каждый раз, когда создается или обновляется позиция заказа, 
    # рассчитывается стоимость этой позиции, и затем обновляется общая стоимость заказа через метод update_total_price.
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        
        # Обновляем общую стоимость заказа
        self.order.update_total_price()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)