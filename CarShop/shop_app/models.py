from django.db import models
import uuid
from django.contrib.auth.models import User
from PIL import Image
from .validators import \
    validate_phone_number, normalize_phone, \
    validate_address, \
    get_positive_validator, \
    get_not_negative_validator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=64, validators=[validate_phone_number],
                             help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = models.CharField(max_length=64, validators=[validate_address])

    avatar = models.ImageField(
        default='default_avatar.jpg',
        upload_to='profile_avatars'
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        self.phone = normalize_phone(self.phone)

        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 320 or img.width > 320:
            output_size = (320, 320)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


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


class Provider(models.Model):
    name = models.CharField(max_length=64, unique=True)

    phone = models.CharField(max_length=64, validators=[validate_phone_number],
                             help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = models.CharField(max_length=64, validators=[validate_address])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/provider/{self.id}/'

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        ordering = ("name",)


class Producer(models.Model):
    name = models.CharField(max_length=64, unique=True)

    phone = models.CharField(max_length=64, validators=[validate_phone_number],
                             help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = models.CharField(max_length=64, validators=[validate_address])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/producer/{self.id}/'

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"
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

    providers = models.ManyToManyField(Provider, help_text="Select a provider for this product")

    producer = models.OneToOneField(Producer, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return f"/product/{self.article}/"

    def get_producer(self):
        return self.producer.name

    def get_few_providers(self):
        max_count = 3
        providers = self.providers.all()

        if len(providers) > max_count:
            return ', '.join([provider.name for provider in providers[:max_count]]) + " and others"
        else:
            return ', '.join([provider.name for provider in providers])

    def get_many_providers(self):
        max_count = 20
        max_str_length = 20
        providers = self.providers.all()

        if len(providers) <= max_count:
            prov_strs = []

            for provider in providers:

                if prov_strs and len(prov_strs[-1]) < max_str_length:
                    prov_strs[-1] += f", {str(provider)}"
                else:
                    prov_strs.append(str(provider))

            return '\n'.join(prov_strs)

        else:
            return f"More than {max_count} providers"

    get_producer.short_description = 'Producer'
    get_few_providers.short_description = 'Providers'
    get_many_providers.short_description = 'Providers'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("name",)

