from django.contrib import admin
from .models import Product, Supplier, Specification



class SpecificationInline(admin.TabularInline):
    model = Specification  # Используем связь через ManyToMany
    extra = 1  # Количество пустых строк для добавления новых спецификаций

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'price', 'stock', 'color')
    inlines = [SpecificationInline]


class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('spec_name', 'spec_value')  # Поля для отображения в админке

admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
admin.site.register(Specification, SpecificationAdmin)
