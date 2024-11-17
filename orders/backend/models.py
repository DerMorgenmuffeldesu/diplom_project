from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator
import re

# Статусы заказа
ORDER_STATUSES = (
    ('basket', 'Корзина'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_ROLES = (
    ('store', 'Магазин'),
    ('customer', 'Покупатель'),
)

class AppUserManager(BaseUserManager):
    """
    Менеджер для пользователей, использующий email вместо имени пользователя.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class AppUser(AbstractUser):
    """
    Расширенная модель пользователя с email и дополнительными полями.
    """
    REQUIRED_FIELDS = []
    objects = AppUserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(choices=USER_ROLES, max_length=10, default='customer')
    is_active = models.BooleanField(default=True)


    groups = models.ManyToManyField(
        Group,
        related_name="appuser_groups",  # Уникальное имя для связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="appuser_permissions",  # Уникальное имя для связи
        blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        # Валидация для поля role
        if self.role not in dict(USER_ROLES).keys():
            raise ValidationError(_('Invalid role'))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Store(models.Model):
    """
    Магазины, которые могут добавлять товары и обрабатывать заказы.
    """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    """
    Категории товаров.
    """
    name = models.CharField(max_length=50)
    stores = models.ManyToManyField(Store, related_name='categories', blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    """
    Продукты, которые продаются в магазинах.
    """
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

class ItemDetails(models.Model):
    """
    Информация о товаре в разных магазинах.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='details')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='details')
    external_id = models.PositiveIntegerField(unique=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    recommended_price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.item.name} ({self.store.name})'

    def clean(self):
        # Валидация: количество и цена должны быть больше нуля
        if self.quantity <= 0:
            raise ValidationError(_('Quantity must be greater than zero'))
        if self.price <= 0:
            raise ValidationError(_('Price must be greater than zero'))
        if self.recommended_price <= 0:
            raise ValidationError(_('Recommended price must be greater than zero'))

class Order(models.Model):
    """
    Заказы пользователей, связанные с товарами и их состоянием.
    """
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(choices=ORDER_STATUSES, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.status}'

    def clean(self):
        # Валидация: статус должен быть в списке допустимых
        if self.status not in dict(ORDER_STATUSES).keys():
            raise ValidationError(_('Invalid status'))

class ItemInOrder(models.Model):
    """
    Позиции товара в заказах.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_details = models.ForeignKey(ItemDetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.item_details.item.name} x {self.quantity}'

class Contact(models.Model):
    """
    Контактная информация пользователя.
    """
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='contacts')
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.city}, {self.phone}'

    def clean(self):
        # Валидация: телефон должен соответствовать формату
        phone_regex = r'^\+?\d{1,3}?\s?\(?\d+\)?\s?\d+$'
        if not re.match(phone_regex, self.phone):
            raise ValidationError(_('Invalid phone number format'))

class EmailConfirmationToken(models.Model):
    """
    Токен для подтверждения email.
    """
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='confirmation_tokens')
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_key():
        return get_token_generator().generate_token()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Email token for {self.user.email}'
