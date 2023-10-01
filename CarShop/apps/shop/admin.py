from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from more_admin_filters import MultiSelectRelatedFilter

from apps.core.admin_tools import (
    admin_override,
    make_range_field_list_filter,
    make_condition_filter,
    ViewOnlyFieldsAdminMixin, create_link_one, create_link_many,
    UserFieldsetsInlineMixin, FieldsWidgetsMixin
)
from apps.core.db_tools import queryset_condition_filter
from .models import Category, Product, Buy, Profile, Provider, CarouselItem, News, Review, Faq, Coupon
from .forms import UserAsProviderChangeForm
from .matchers import match_phone_number, match_date, match_address, match_content
from .validators import validate_provider, is_valid
from django.forms import ModelForm, Textarea


admin.site.empty_value_display = '???'

QuerySet.condition_filter = queryset_condition_filter


class ProfileInline(FieldsWidgetsMixin, admin.StackedInline):
    model = Profile
    fields = ('avatar', 'phone', 'address', 'coupons')

    # This field is also used by m2m inlines, where there can be more than one inline.
    # This ensures that inlines fields are required when creating a user.
    min_num = max_num = 1

    can_delete = False

    fields_widgets = {
        'coupons': admin.widgets.FilteredSelectMultiple('Coupons', False)
    }


@admin_override(User)
class UserProfileAdmin(UserFieldsetsInlineMixin, UserAdmin):
    form = UserAsProviderChangeForm

    inlines = (ProfileInline,)

    list_display = ('username', 'get_avatar_as_html_image', 'email', 'first_name', 'last_name',
                    'get_address', 'get_phone')

    list_display_links = ('username', 'get_avatar_as_html_image')

    ordering = ('username',)

    provider_filter = make_condition_filter(is_valid(validate_provider), "provider status", "provider_status")
    list_filter = ('is_staff', 'is_superuser', provider_filter)

    search_fields = ('username', 'email', 'first_name', 'last_name')  # + profile__phone, profile__address

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image_as_html_image', 'get_logo_as_html_image')
    list_display_links = ('name', 'get_image_as_html_image', 'get_logo_as_html_image')

    fields = ('name', 'image_key', 'image', 'logo')

    readonly_fields = ("image_key",)

    def get_logo_as_html_image(self, obj):
        return obj.get_logo_as_html_image(height=75)

    def get_image_as_html_image(self, obj):
        return obj.get_image_as_html_image(height=75)

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
    list_display = ('name', 'get_image_as_html_image', 'category', 'price', 'get_providers_as_link')
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
            'fields': ('article', 'image_key', 'providers')
        }),
    )

    viewonly_fields = ('category', 'providers')
    readonly_fields = ("article", 'image_key')

    list_per_page = 20

    def get_providers_as_link(self, obj):
        providers = obj.providers.all()

        if len(providers) == 1:
            return create_link_one(
                User.objects.filter(id=providers[0].id)[0],
                obj.get_few_providers()
            )
        else:
            return create_link_many(
                User.objects.filter(id__in=[p.id for p in providers]),
                obj.get_few_providers()
            )

    get_providers_as_link.short_description = "Providers"

    def get_image_as_html_image(self, obj):
        return obj.get_image_as_html_image(height=100)

    get_image_as_html_image.short_description = "Image"


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ('date', 'get_user_as_link', 'get_product_as_link', 'count', 'card_num')
    ordering = ('-date', 'user', 'product', 'count')
    list_filter = (
        ('date', DateFieldListFilter),
    )

    fields = ("date", "user", 'product', 'count', 'card_num')

    search_fields = ('count', 'user__username', 'product__name') # + date

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

    def get_user_as_link(self, obj):
        return create_link_one(obj.user, obj.user.username)

    get_user_as_link.short_description = "Providers"

    def get_product_as_link(self, obj):
        return create_link_one(obj.product, obj.product.name)

    get_product_as_link.short_description = "Product"

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'product', 'date')
    ordering = ('user', 'product', '-date')
    list_filter = (
        ('user', MultiSelectRelatedFilter),
        ('product', MultiSelectRelatedFilter),
        ('date', DateFieldListFilter),
    )

    fields = ("user", "product", 'date', 'content')

    search_fields = ('user__username', 'product__name') # + date

    def get_search_results(self, request, queryset, search_term):
        date_matches = queryset.condition_filter(lambda obj: match_date(obj.date, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return date_matches | other_matches, may_have_duplicates

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    ordering = ('-date', 'title')
    list_filter = (('date', DateFieldListFilter), )

    fields = ("title", 'date', 'content')
    readonly_fields = ('date', )

    search_fields = ('title', ) # + date, content

    def get_search_results(self, request, queryset, search_term):
        date_matches = queryset.condition_filter(lambda obj: match_date(obj.date, search_term) > 0.75)
        content_matches = queryset.condition_filter(lambda obj: match_content(obj.content, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return (date_matches | content_matches | other_matches), may_have_duplicates


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    ordering = ('-date', 'title')
    list_filter = (('date', DateFieldListFilter), )

    fields = ("title", 'date', 'content')
    readonly_fields = ('date', )

    search_fields = ('title', ) # + date, content

    def get_search_results(self, request, queryset, search_term):
        date_matches = queryset.condition_filter(lambda obj: match_date(obj.date, search_term) > 0.75)
        content_matches = queryset.condition_filter(lambda obj: match_content(obj.content, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return (date_matches | content_matches | other_matches), may_have_duplicates


@admin.register(CarouselItem)
class CarouselItemAdmin(FieldsWidgetsMixin, admin.ModelAdmin):
    list_display = ('get_image_as_html_image', 'get_context_text')
    list_display_links = ('get_image_as_html_image', 'get_context_text')
    ordering = ('id', )

    search_fields = ('content', )

    list_per_page = 20

    fields_widgets = {
        'content': Textarea(attrs={'cols': 140, 'rows': 20})
    }

    def get_image_as_html_image(self, obj):
        return obj.get_image_as_html_image(height=100)

    def get_context_text(self, obj):
        return obj.get_context_text()

    get_image_as_html_image.short_description = "Image"
    get_context_text.short_description = "Text"

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
