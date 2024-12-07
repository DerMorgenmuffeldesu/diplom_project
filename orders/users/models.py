from django.db import models
from django.contrib.auth.models import User
from .tasks import process_avatar
from django.core.exceptions import ValidationError
import logging




logger = logging.getLogger(__name__)

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        logger.info("Start saving profile")
        super().save(*args, **kwargs)
        logger.info("Profile saved successfully")
        if self.avatar:
            process_avatar.delay(self.avatar.path, [(100, 100), (200, 200)])

    def clean(self):
        # Ограничение размера файла до 2MB
        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 2MB.")


    def __str__(self):
        return self.user.username


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.country}"