from django.db import models
import uuid


class Category(models.Model):
    name = models.CharField(max_length=64, help_text="Enter a category (e.g. Oil, Tire etc.)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("name",)


class Provider(models.Model):
    name = models.CharField(max_length=64)

    phone = models.CharField(max_length=64)

    address = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        ordering = ("name",)


class Producer(models.Model):
    name = models.CharField(max_length=64)

    phone = models.CharField(max_length=64)

    address = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"
        ordering = ("name",)


class Buy(models.Model):
    date = models.DateField()

    product_name = models.CharField(max_length=64, help_text="Name of product")

    count = models.IntegerField()

    def __str__(self):
        return f"buy {{ date: {self.date}, product: {self.product_name}, count: {self.count} }}"

    class Meta:
        verbose_name = "Buy"
        verbose_name_plural = "Buys"
        ordering = ("-date", "product_name", "count")


class Product(models.Model):
    name = models.CharField(max_length=64)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    article = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for this product")

    price = models.IntegerField()

    providers = models.ManyToManyField(Provider, help_text="Select a provider for this product")

    producer = models.OneToOneField(Producer, on_delete=models.CASCADE)

    def display_producer(self):
        return self.producer.name

    def display_few_providers(self):
        max_count = 3
        providers = self.providers.all()

        if len(providers) > max_count:
            return ', '.join([provider.name for provider in providers[:max_count]]) + " and others"
        else:
            return ', '.join([provider.name for provider in providers])

    def display_many_providers(self):
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
            return "More than 20 providers"

    display_producer.short_description = 'Producer'
    display_few_providers.short_description = 'Providers'
    display_many_providers.short_description = 'Providers'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("name",)

