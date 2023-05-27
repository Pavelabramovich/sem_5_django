from django.db import models
import uuid


class ProductType(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a product type (e.g. Oil, Tire etc.)")

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=50)

    phone = models.CharField(max_length=50)

    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()


class Producer(models.Model):
    name = models.CharField(max_length=50)

    phone = models.CharField(max_length=50)

    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)

    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    article = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for this product")

    price = models.IntegerField()

    providers = models.ManyToManyField(Provider, help_text="Select a provider for this product")

    producer = models.OneToOneField(Producer, on_delete=models.CASCADE)

    def display_producer(self):
        return self.producer.name
    display_producer.short_description = 'Producer'

    def display_short_providers(self):
        providers = self.providers.all()

        if len(providers) > 3:
            return ', '.join([provider.name for provider in providers[:3]]) + " and others"
        else:
            return ', '.join([provider.name for provider in providers])

    display_short_providers.short_description = 'Providers'

    def display_all_providers(self):
        providers = self.providers.all()

        if len(providers) <= 20:
            prov_strs = []

            for provider in providers:

                if prov_strs and len(prov_strs[-1]) < 20:
                    prov_strs[-1] += f", {str(provider)}"
                else:
                    prov_strs.append(str(provider))

            return '\n'.join(prov_strs)

        else:
            return "More than 20 providers"

    display_all_providers.short_description = 'All providers'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('book-detail', args=[str(self.id)])
