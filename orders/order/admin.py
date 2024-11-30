from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'get_total_quantity_display', 'get_total_amount', 'created_at', 'shipping_address')
    inlines = [OrderProductInline]
    readonly_fields = ('customer', 'created_at', 'total_amount',)  # Если вы не хотите, чтобы эти поля редактировались
    
    def get_total_quantity_display(self, obj):
        return obj.get_total_quantity()

    get_total_quantity_display.short_description = 'Total Quantity'


admin.site.register(Order, OrderAdmin)

