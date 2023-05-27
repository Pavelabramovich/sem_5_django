from django.contrib import admin
from .models import ProductType, Provider, Producer, Product


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'display_producer', 'display_short_providers')

    fieldsets = (
        (None, {
            'fields': ('name', 'product_type', 'price')
        }),
        ('Detailed information', {
            'fields': ('article', 'producer', 'providers')
        }),
    )


admin.site.register(ProductType)

admin.site.register(Provider, ProviderAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Product, ProductAdmin)
