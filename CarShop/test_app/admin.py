from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Category, Producer, Provider, Product, Buy
from .forms import CategoryForm, ProducerForm, ProviderForm, ProductForm, BuyForm
from .make_range_field_list_filter import make_range_field_list_filter
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from more_admin_filters import MultiSelectRelatedFilter, MultiSelectFilter
from .matchers import match_phone_number, match_date, match_address

admin.site.empty_value_display = '???'


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
class ProviderAdmin(admin.ModelAdmin):
    form = ProviderForm

    list_display = ('name', 'phone', 'address')
    ordering = ('name', 'phone')
    list_editable = ('phone', 'address')

    search_fields = ("name",)

    def get_search_results(self, request, queryset, search_term):
        phone_matches_id = {obj.id for obj in queryset if
                            match_phone_number(obj.phone, search_term) > 0.75}

        address_matches_id = {obj.id for obj in queryset if
                              match_address(obj.address, search_term) > 0.75}

        filtered_id = phone_matches_id | address_matches_id

        filtered_queryset = queryset.filter(id__in=filtered_id)

        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return queryset | filtered_queryset, may_have_duplicates

    search_help_text = "Enter provider name, phone number or address"

    list_per_page = 20


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    form = ProducerForm

    list_display = ('name', 'phone', 'address')
    ordering = ('name', 'phone')
    list_editable = ('phone', 'address')

    search_fields = ("name",)

    def get_search_results(self, request, queryset, search_term):
        phone_matches_id = {obj.id for obj in queryset if
                            match_phone_number(obj.phone, search_term) > 0.75}

        address_matches_id = {obj.id for obj in queryset if
                              match_address(obj.address, search_term) > 0.75}

        filtered_id = phone_matches_id | address_matches_id

        filtered_queryset = queryset.filter(id__in=filtered_id)

        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return queryset | filtered_queryset, may_have_duplicates

    search_help_text = "Enter producer name, phone number or address"

    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

    list_display = ('name', 'category', 'price', 'get_producer_as_link', 'get_providers_as_link')
    ordering = ('name', 'category', 'price')

    price_range_list_filter = make_range_field_list_filter([
        ("$0 - $10", 0, 10),
        ("$10 - $50", 10, 50),
        ("$50 - $100", 50, 100),
        ("$100 and more", 100, None),
    ])

    list_filter = (
        ('category', MultiSelectRelatedFilter),
        ('price', price_range_list_filter),
        ('providers', MultiSelectRelatedFilter)
    )
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

    readonly_fields = ("article",)

    list_per_page = 20

    def get_producer_as_link(self, obj):
        producer = obj.producer

        link = (
                reverse("admin:test_app_producer_changelist") +
                "?" +
                urlencode({"id": producer.id})
        )

        return format_html('<b><a href="{}">{}</a></b>', link, producer)

    def get_providers_as_link(self, obj):
        providers = obj.providers.all()
        providers_id = ','.join([str(provider.id) for provider in providers])

        link = (
                reverse("admin:test_app_provider_changelist") +
                "?" +
                urlencode({"id__in": providers_id})
        )

        few_providers = obj.get_few_providers()

        return format_html('<a href="{}">{}</a>', link, few_providers)

    get_producer_as_link.short_description = "Producer"
    get_providers_as_link.short_description = "Providers"


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    form = BuyForm

    list_display = ('date', 'product_name', 'count')
    ordering = ('date', 'product_name', 'count')
    list_filter = (('date', DateFieldListFilter), ('product_name', MultiSelectFilter))

    search_fields = ('product_name',)

    def get_search_results(self, request, queryset, search_term):
        date_matches_id = {obj.id for obj in queryset if
                           match_date(obj.date, search_term) > 0.75}

        filtered_queryset = queryset.filter(id__in=date_matches_id)

        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return queryset | filtered_queryset, may_have_duplicates

    search_help_text = "Enter product name or date of buy"

    list_per_page = 20

    def has_change_permission(self, request, obj=None):
        return False
