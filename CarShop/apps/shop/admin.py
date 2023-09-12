from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from more_admin_filters import MultiSelectRelatedFilter, MultiSelectFilter

from apps.core.admin_tools import (
    admin_override,
    make_range_field_list_filter,
    make_condition_filter,
    ViewOnlyFieldsAdminMixin,
    UserFieldsetsInlineMixin
)
from apps.core.db_tools import queryset_condition_filter
from .models import Category, Product, Buy, Profile, Provider, CarouselItem, News, Review, Faq, Coupon
from .forms import UserAsProviderChangeForm, NewsModelForm, ReviewModelForm, FaqModelForm
from .matchers import match_phone_number, match_date, match_address
from .validators import validate_provider, is_valid

admin.site.empty_value_display = '???'

admin.override = admin_override
QuerySet.condition_filter = queryset_condition_filter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image_as_html_image', 'get_logo_as_html_image')

    fieldsets = (
        (None, {
            'fields': ('name', 'uuid', 'image', 'logo')
        }),
    )

    readonly_fields = ("uuid",)

    def get_logo_as_html_image(self, obj):
        return obj.get_logo_as_html_image(width=75)

    def get_image_as_html_image(self, obj):
        return obj.get_image_as_html_image(width=75)

    get_logo_as_html_image.short_description = "Logo"
    get_image_as_html_image.short_description = "Image"

    ordering = ('name',)
    search_fields = ("name",)

    list_per_page = 20

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(Product)
class ProductAdmin(ViewOnlyFieldsAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'get_providers_as_link')
    ordering = ('name', 'category', 'price')

    price_range_list_filter = make_range_field_list_filter([
        ("$0 - $10", 0, 10),
        ("$10 - $50", 10, 50),
        ("$50 - $100", 50, 100),
        ("$100 and more", 100, None)
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
            'fields': ('name', 'category', 'price', 'image')
        }),
        ('Detailed information', {
            'fields': ('article', 'uuid', 'providers')
        }),
    )

    viewonly_fields = ('category', 'providers')
    readonly_fields = ("article", 'uuid')

    list_per_page = 20

    def get_providers_as_link(self, obj):
        providers = obj.providers.all()
        providers_id = ','.join([str(provider.id) for provider in providers])

        link = (
                reverse("admin:auth_user_changelist") +
                "?" +
                urlencode({"id__in": providers_id})
        )

        few_providers = obj.get_few_providers()

        return format_html('<a href="{}">{}</a>', link, few_providers)

    get_providers_as_link.short_description = "Providers"


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'product', 'count', 'card_num')
    ordering = ('date', 'product', 'count')
    list_filter = (
        ('date', DateFieldListFilter),
        ('user', MultiSelectRelatedFilter),
        ('product', MultiSelectRelatedFilter)
    )

    search_fields = ('count',)

    def get_search_results(self, request, queryset, search_term):
        date_matches = queryset.condition_filter(lambda obj: match_date(obj.date, search_term) > 0.75)

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

    def has_add_permission(self, request):
        return False


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ('avatar', 'phone', 'address')

    verbose_name_plural = 'Profile'

    # This ensures that inlines fields are required when creating a user.
    min_num = 1
    can_delete = False

    classes = ('no-upper', 'no-title')

    class Media:
        css = {
            'all': ('admin/css/admin_inline_style.css',)
        }


@admin.override(User)
class UserProfileAdmin(UserFieldsetsInlineMixin, UserAdmin):
    form = UserAsProviderChangeForm

    inlines = (ProfileInline,)

    list_display = ('username', 'get_avatar_as_html_image', 'email', 'first_name', 'last_name',
                    'get_address', 'get_phone')

    list_display_links = ('username', 'get_avatar_as_html_image')

    ordering = ('username',)

    provider_filter = make_condition_filter(is_valid(validate_provider), "provider status", "provider_status")
    list_filter = ('is_staff', 'is_superuser', provider_filter)

    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_search_results(self, request, queryset, search_term):
        check_high_phone_match = lambda obj: match_phone_number(obj.profile.phone, search_term) > 0.75
        check_high_address_match = lambda obj: match_address(obj.profile.address, search_term) > 0.85

        phone_matches = queryset.condition_filter(check_high_phone_match)
        address_matches = queryset.condition_filter(check_high_address_match)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return phone_matches | address_matches | other_matches, may_have_duplicates

    search_help_text = "Enter username, email, first name, last name, phone number or address"

    fieldsets_with_inlines = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ProfileInline,
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'is_provider', 'groups', "user_permissions", 'products')
        })
    )

    add_fieldsets_with_inlines = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ProfileInline,
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', "user_permissions")
        })
    )

    readonly_fields = ('last_login', 'date_joined')

    def get_phone(self, obj):
        return obj.profile.phone

    def get_address(self, obj):
        return obj.profile.address

    def get_avatar_as_html_image(self, obj):
        return obj.profile.get_avatar_as_html_image(size=65)

    get_phone.short_description = "Phone"
    get_address.short_description = "Address"
    get_avatar_as_html_image.short_description = "Avatar"

    list_per_page = 20

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsModelForm


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    form = FaqModelForm


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    fields = ('discount', 'user')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewModelForm

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('get_image_as_html_image', 'title', 'subtitle')
    list_editable = ('title', 'subtitle')
    ordering = ('title', 'subtitle')

    search_fields = ('title', 'subtitle')

    list_per_page = 20

    def get_image_as_html_image(self, obj):
        return obj.get_image_as_html_image(height=100)

    get_image_as_html_image.short_description = "Image"

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
