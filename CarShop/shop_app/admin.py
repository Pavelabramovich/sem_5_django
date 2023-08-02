from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Category, Producer, Provider, Product, Buy, Profile
from .forms import CategoryForm, ProducerForm, ProviderForm, ProductForm, BuyForm, ProfileForm
from .make_range_field_list_filter import make_range_field_list_filter
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from more_admin_filters import MultiSelectRelatedFilter, MultiSelectFilter
from .matchers import match_phone_number, match_date, match_address
from .admin_override import override
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from fieldsets_with_inlines import FieldsetsInlineMixin

from .queryset_lambda_filter import queryset_lambda_filter

admin.site.empty_value_display = '???'
admin.override = override


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
        phone_matches = queryset_lambda_filter(queryset, lambda obj: match_phone_number(obj.phone, search_term) > 0.75)
        address_matches = queryset_lambda_filter(queryset, lambda obj: match_address(obj.address, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return phone_matches | address_matches | other_matches, may_have_duplicates

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
        phone_matches = queryset_lambda_filter(queryset, lambda obj: match_phone_number(obj.phone, search_term) > 0.75)
        address_matches = queryset_lambda_filter(queryset, lambda obj: match_address(obj.address, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return phone_matches | address_matches | other_matches, may_have_duplicates

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
        date_matches = queryset_lambda_filter(queryset, lambda obj: match_date(obj.date, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return date_matches | other_matches, may_have_duplicates

    search_help_text = "Enter product name or date of buy"

    list_per_page = 20

    def has_change_permission(self, request, obj=None):
        return False


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


@admin.override(User)
class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserProfileAdmin, self).get_inline_instances(request, obj)

    list_display = ('username', 'email', 'first_name', 'last_name', 'get_address', 'get_phone')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_search_results(self, request, queryset, search_term):
        check_high_phone_match = lambda obj: match_phone_number(obj.profile.phone, search_term) > 0.75
        check_high_address_match = lambda obj: match_phone_number(obj.profile.address, search_term) > 0.75

        phone_matches = queryset_lambda_filter(queryset, check_high_phone_match)
        address_matches = queryset_lambda_filter(queryset, check_high_address_match)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return phone_matches | address_matches | other_matches, may_have_duplicates

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
       # ProfileInline,
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        })
    )

    def get_phone(self, obj):
        return obj.profile.phone

    def get_address(self, obj):
        return obj.profile.address

    get_phone.short_description = "Phone"
    get_address.short_description = "Address"

    list_per_page = 20
