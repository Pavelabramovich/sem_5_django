from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Category, Producer, Provider, Product, Buy
from .forms import CategoryForm, ProducerForm, ProviderForm, ProductForm, BuyForm
from .make_range_field_list_filter import make_range_field_list_filter
from .make_validated_list_editable_admin_formset import make_validated_list_editable_admin_formset
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


class ValidatedListEditableAdmin(admin.ModelAdmin):
    def get_changelist_formset(self, request, **kwargs):
        kwargs['formset'] = make_validated_list_editable_admin_formset(self.form)
        return super().get_changelist_formset(request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm

    list_display = ('name',)
    list_display_links = None
    list_editable = ('name',)
    ordering = ('name',)
    search_fields = ("name",)

    list_per_page = 20


@admin.register(Provider)
class ProviderAdmin(ValidatedListEditableAdmin):
    form = ProviderForm

    list_display = ('name', 'phone', 'address')
    ordering = ('name', 'phone')
    list_editable = ('phone', 'address')
    search_fields = ("name",)

    list_per_page = 20


@admin.register(Producer)
class ProducerAdmin(ValidatedListEditableAdmin):
    form = ProducerForm

    list_display = ('name', 'phone', 'address')
    ordering = ('name', 'phone')
    list_editable = ('phone', 'address')
    search_fields = ("name",)

    list_per_page = 20


@admin.register(Product)
class ProductAdmin(ValidatedListEditableAdmin):
    form = ProductForm

    list_display = ('name', 'category', 'price', 'display_producer_as_link', 'display_few_providers')
    ordering = ('name', 'category', 'price')

    price_range_list_filter = make_range_field_list_filter([
        ("$0 - $10", 0, 10),
        ("$10 - $50", 10, 50),
        ("$50 - $100", 50, 100),
        ("$100 and more", 100, None),
    ])

    list_filter = ('category', ('price', price_range_list_filter), 'providers')
    list_editable = ('category', 'price')
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'price')
        }),
        ('Detailed information', {
            'fields': ('article', 'producer', 'providers')
        }),
    )

    list_per_page = 20

    def display_producer_as_link(self, obj):
        producer = obj.producer

        link = (reverse("admin:test_app_producer_changelist") + "?" + urlencode({"id": producer.id}))

        return format_html('<b><a href="{}">{}</a></b>', link, producer)

    display_producer_as_link.short_description = "Producer"


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    form = BuyForm

    list_display = ('date', 'product_name', 'count')
    ordering = ('date', 'product_name', 'count')
    list_filter = (('date', DateFieldListFilter), 'product_name')
    search_fields = ('product_name',)

    list_per_page = 20

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
