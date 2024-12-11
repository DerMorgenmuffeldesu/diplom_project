from django.contrib import admin
from .models import Order, OrderProduct
from django import forms


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 0


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


@admin.action(description="Подтвердить выбранные заказы")
def confirm_orders(modeladmin, request, queryset):
    queryset.update(status='confirmed')


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('id', 'customer', 'status', 'get_total_quantity_display', 'get_total_amount', 'created_at', 'shipping_address')
    inlines = [OrderProductInline]
    readonly_fields = ('customer', 'created_at', 'total_amount',)  # Если вы не хотите, чтобы эти поля редактировались
    actions = [confirm_orders]
    
    def get_total_quantity_display(self, obj):
        return obj.get_total_quantity()

    get_total_quantity_display.short_description = 'Total Quantity'


@admin.action(description="Отменить выбранные заказы")
def cancel_orders(modeladmin, request, queryset):
    queryset.update(status='canceled')

actions = [confirm_orders, cancel_orders]




admin.site.register(Order, OrderAdmin)

