from django.contrib import admin
from .models import Profile



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'email', 'avatar')

    #Метод для получения username из связанного пользователя
    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'  # Для сортировки
    get_username.short_description = 'Username'  # Название в списке
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Убедитесь, что метод save модели Profile вызывается
        obj.save()



admin.site.register(Profile, ProfileAdmin)