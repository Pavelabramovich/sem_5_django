import uuid

from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from apps.core.model_tools import AvatarField
from .validators import (
    validate_phone_number, normalize_phone,
    validate_address,
    get_positive_validator,
    get_not_negative_validator, validate_provider
)
from apps.core.media_tools import OverwriteCodedStorage
from apps.core.model_tools import SvgField, NamedImageField
import apps.shop.model_funcs as model_funcs


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=64, validators=[validate_phone_number],
                             help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = models.CharField(max_length=64, validators=[validate_address])

    avatar = AvatarField(upload_to='profile_avatars', default='profile_avatars/avatar_default.jpg', blank=True,
                         get_color=model_funcs.get_profile_avatar_color, avatar_size=300,
                         get_filename=model_funcs.get_profile_avatar_filename)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_phone(self.phone)

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.avatar.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)

    def get_avatar_as_html_image(self, size):
        return mark_safe(f'<img src = "{self.avatar.url}" width = "{size}"/>')

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"


class Category(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=64, unique=True,
                            help_text="Enter a category (e.g. Oil, Tire etc.)")

    logo = SvgField(upload_to='categories_logo', default='categories_logo/logo_default.svg',
                    get_filename=model_funcs.get_category_logo_filename, storage=OverwriteCodedStorage())

    image = NamedImageField(upload_to='categories_images', default='categories_images/image_default.png',
                            get_filename=model_funcs.get_category_image_filename, storage=OverwriteCodedStorage())

    def delete(self, using=None, keep_parents=False):
        if self.logo != self.logo.field.default:
            self.logo.delete(save=False)

        if self.image != self.image.field.default:
            self.image.delete(save=False)

        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/category/{self.id}/'

    def get_logo_as_html_image(self, width):
        return mark_safe(f'<img src = "{self.logo.url}" width = "{width}"/>')

    def get_image_as_html_image(self, width):
        return mark_safe(f'<img src = "{self.image.url}" width = "{width}"/>')

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
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
        verbose_name = "buy"
        verbose_name_plural = "buys"
        ordering = ("-date", "product_name", "count")


class Provider(User):
    pass


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    article = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                               help_text="Unique ID for this product")

    price = models.IntegerField(validators=[get_not_negative_validator('Price')])

    providers = models.ManyToManyField(Provider, help_text="Select a provider for this product",
                                       blank=True, related_name='products')

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
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ("name",)


class CarouselItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    image = NamedImageField(upload_to='carousel_items_images',
                            get_filename=model_funcs.get_carousel_item_image_filename, storage=OverwriteCodedStorage())

    title = models.CharField(max_length=64, blank=True)
    subtitle = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.title

    def get_image_as_html_image(self, height):
        return mark_safe(f'<img src = "{self.image.url}" height = "{height}"/>')
