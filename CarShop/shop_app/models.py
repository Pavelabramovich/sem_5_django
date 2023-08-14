from datetime import datetime

from django.db import models, transaction
import uuid
import random
import os
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from PIL import Image
from .img_tools import crop_to_circle, create_background
from .m2m_validation import ChoicesValidatedManyToManyField
from .overwrite_storage import OverwriteStorage, AvatarStorage, AvatarField

from .validators import \
    validate_phone_number, normalize_phone, \
    validate_address, \
    get_positive_validator, \
    get_not_negative_validator, validate_provider


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=64, validators=[validate_phone_number],
                             help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = models.CharField(max_length=64, validators=[validate_address])

    avatar = AvatarField(upload_to='profile_avatars', blank=True,
                               default='profile_avatars/avatar_default.jpg', storage=AvatarStorage())
    AVATAR_SIZE = 300

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_phone(self.phone)

        super().save(*args, **kwargs)

        # # with transaction.atomic():
        # user_id = self.user.id
        #
        # if self.avatar and self.avatar.name != self.avatar.field.default:
        #     with Image.open(self.avatar.path) as image:
        #         square_avatar = image.copy()
        #
        #     os.remove(self.avatar.path)
        # else:
        #     random.seed(user_id)
        #     avatar_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #     avatar_background = create_background((self.AVATAR_SIZE, self.AVATAR_SIZE), avatar_color)
        #
        #     default_avatar_path = self.avatar.storage.path(self.avatar.field.default)
        #     default_avatar = Image.open(default_avatar_path).convert('RGBA')
        #
        #     square_avatar = Image.alpha_composite(avatar_background, default_avatar)
        #
        # new_avatar = crop_to_circle(square_avatar, self.AVATAR_SIZE)
        #
        # blob = BytesIO()
        # new_avatar.save(blob, 'PNG')
        #
        # self.avatar.save(f"avatar_{user_id}.png", File(blob), save=False)
        #
        # super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        os.remove(self.avatar.path)
        super().delete(using=using, keep_parents=keep_parents)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            help_text="Enter a category (e.g. Oil, Tire etc.)")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/category/{self.id}/'

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("name",)


class Buy(models.Model):
    date = models.DateField()

    product_name = models.CharField(max_length=64, help_text="Name of product")

    count = models.IntegerField(validators=[get_positive_validator('Count')])

    def __str__(self):
        return f"Buy {self.product_name} x{self.count}"

    def get_absolute_url(self):
        return f'buy/{self.id}/'

    class Meta:
        verbose_name = "Buy"
        verbose_name_plural = "Buys"
        ordering = ("-date", "product_name", "count")


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    article = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for this product")

    price = models.IntegerField(validators=[get_not_negative_validator('Price')])

    providers = ChoicesValidatedManyToManyField(User, help_text="Select a provider for this product",
                                                validators=[validate_provider], blank=True, related_name='products')

    def get_absolute_url(self):
        return f"/product/{self.article}/"

    def get_few_providers(self):
        max_count = 3
        providers = self.providers.all()

        if len(providers) > max_count:
            # We cut one less to replace more than one provider.
            return ', '.join([provider.username for provider in providers[:max_count - 1]]) + " and others"
        else:
            return ', '.join([provider.username for provider in providers])

    get_few_providers.short_description = 'Providers'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("name",)

        permissions = [
            ("provide_product", "Can provide Products")
        ]
