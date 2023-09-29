import datetime
import uuid

from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from apps.core.model_tools import AvatarField, IntegerRangeField
from .validators import (
    validate_phone_number, normalize_phone,
    validate_address
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

    coupons = models.ManyToManyField('Coupon', help_text="Select a coupon for this user",
                                     blank=True, related_name='users')

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
        return mark_safe(f'<img src = "{self.avatar.url}" width="{size}" />')

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"


class Provider(User):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            help_text="Enter a category (e.g. Oil, Tire etc.)")
    image_key = models.UUIDField(default=uuid.uuid4, editable=False)

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

    def get_logo_as_html_image(self, *, height, width=None):
        return mark_safe(f'<img src="{self.logo.url}" height="{height}" {f"width={width}" if width else ""} />')

    def get_image_as_html_image(self, *, height, width=None):
        return mark_safe(f'<img src="{self.image.url}" height="{height}" {f"width={width}" if width else ""} />')

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    article = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                               help_text="Unique ID for this product")

    price = IntegerRangeField(min_value=0)

    providers = models.ManyToManyField(Provider, help_text="Select a provider for this product",
                                       blank=True, related_name='products')

    image_key = models.UUIDField(default=uuid.uuid4, editable=False)

    image = NamedImageField(upload_to='products_images',
                            get_filename=model_funcs.get_product_image_filename, storage=OverwriteCodedStorage())

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

    def get_image_as_html_image(self, *, height, width=None):
        return mark_safe(f'<img src="{self.image.url}" height="{height}" {f"width={width}" if width else ""} />')

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ("name",)


class Buy(models.Model):
    date = models.DateField(auto_now_add=True, editable=False)

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', null=True, on_delete=models.CASCADE)

    count = IntegerRangeField(min_value=1)
    card_num = IntegerRangeField(min_value=0, max_value=1000000)

    def __str__(self):
        return f"Buy {self.product.name} x{self.count} by {self.user}"

    def get_absolute_url(self):
        return f'buy/{self.id}/'

    class Meta:
        verbose_name = "buy"
        verbose_name_plural = "buys"
        ordering = ("-date", "product", 'user', "count")


class Coupon(models.Model):
    discount = IntegerRangeField(min_value=1, max_value=100)

    def __str__(self):
        return f"-{self.discount} %"

    def get_absolute_url(self):
        return f"/coupon/{self.id}/"


class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True, editable=False)
    content = models.TextField()

    def __str__(self):
        # The first 3 words are taken and if their length exceeds 15 then a words are slice.
        return (' '.join(str(self.content).split()[:3]))[:15] + '...'

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"


class News(models.Model):
    date = models.DateField(auto_now_add=True, editable=False)

    title = models.CharField(max_length=64, blank=True)
    content = models.TextField()

    image_key = models.UUIDField(default=uuid.uuid4, editable=False)

    image = NamedImageField(upload_to='news_images', blank=True,
                            get_filename=model_funcs.get_news_image_filename, storage=OverwriteCodedStorage())

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/news/{self.id}/"


class Faq(models.Model):
    date = models.DateField(auto_now_add=True, editable=False)

    title = models.CharField(max_length=64, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/faq/{self.id}/"


class CarouselItem(models.Model):
    image_key = models.UUIDField(default=uuid.uuid4, editable=False)

    image = NamedImageField(upload_to='carousel_items_images',
                            get_filename=model_funcs.get_carousel_item_image_filename, storage=OverwriteCodedStorage())

    content = models.TextField(default="""
    <div style="text-align: center;color: #f2f2f2;font-size: 15px;">
        <h1 style='margin-bottom:100px; font: 62.5% "Roboto","Arial","Helvetica",sans-serif; font-size: 5em; font-weight: 700;'>
            Create
        </h1>
        <h3 style='font: 62.5% "Roboto","Arial","Helvetica",sans-serif; font-size: 1.9em;'>
            Our workers are the best
        </h3>
    </div>
    """.replace('\n    ', '\n').replace('\n', '', 1))

    def __str__(self):
        return (' '.join(str(self.content).split()[:3]))[:15] + '...'

    def get_image_as_html_image(self, *, height, width=None):
        return mark_safe(f'<img src="{self.image.url}" height="{height}" {f"width={width}" if width else ""} />')

    def delete(self, using=None, keep_parents=False):
        self.image.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        ordering = ("id", )











