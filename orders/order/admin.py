from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'status')  # Используем правильные поля

    def get_order_date(self, obj):
        return obj.created_at.date()  # Например, выводим только дату, без времени
    get_order_date.short_description = 'Order Date'

admin.site.register(Order, OrderAdmin)
