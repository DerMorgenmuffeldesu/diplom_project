from django.contrib import admin
from .models import AppUser, Store, Category, Item, Order

admin.site.register(AppUser)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
