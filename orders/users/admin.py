from django.contrib import admin
from .models import Profile, ShippingAddress
from django.utils.html import mark_safe



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'email', 'avatar')
    search_fields = ('user__username', 'email')
    list_filter = ('user__is_staff', 'user__is_active')



    #Метод для получения username из связанного пользователя
    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'  # Для сортировки
    get_username.short_description = 'Username'  # Название в списке
    
    def save_model(self, request, obj, form, change):
        if obj.user.email != obj.email:
            obj.user.email = obj.email  # Обновляем email в связанном User
            obj.user.save()
        super().save_model(request, obj, form, change)

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" height="50" />')
        return "Нет аватара"
    get_avatar.short_description = 'Avatar'

admin.site.register(Profile, ProfileAdmin)