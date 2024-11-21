from django.contrib import admin
from .models import Product, Supplier


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'price', 'stock')


admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
