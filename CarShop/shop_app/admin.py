from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Category, Producer, Provider, Product, Buy, Profile
from .make_range_field_list_filter import make_range_field_list_filter
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from more_admin_filters import MultiSelectRelatedFilter, MultiSelectFilter
from .matchers import match_phone_number, match_date, match_address
from .admin_override import override
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .fieldsets_inline_mixin import FieldsetsInlineMixin, UserFieldsetsInlineMixin
from django.db.models.query import QuerySet
from django.utils.html import mark_safe


from django.template.loader import get_template


from .queryset_condition_filter import queryset_condition_filter

admin.site.empty_value_display = '???'

admin.override = override
QuerySet.condition_filer = queryset_condition_filter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_display_links = None
    list_editable = ('name',)
    ordering = ('name',)

    search_fields = ("name",)

    list_per_page = 20


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):

    list_display = ('name', 'phone', 'address')
    ordering = ('name', 'phone')
    list_editable = ('phone', 'address')

    search_fields = ("name",)

    def get_search_results(self, request, queryset, search_term):
        phone_matches = queryset.condition_filer(lambda obj: match_phone_number(obj.phone, search_term) > 0.75)
        address_matches = queryset.condition_filer(lambda obj: match_address(obj.address, search_term) > 0.75)

        (other_matches, may_have_duplicates) = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        print(get_template('admin/change_form.html').backend.template_dirs[0])

        return phone_matches | address_matches | other_matches, may_have_duplicates

    search_help_text = "Enter provider name, phone number or address"

    list_per_page = 20


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):

    list_display = ('name', 'phone', 'address')
    ordering = ('name', 'phone')
    list_editable = ('phone', 'address')

    search_fields = ("name",)

    def get_search_results(self, request, queryset, search_term):
        phone_matches = queryset.condition_filer(lambda obj: match_phone_number(obj.phone, search_term) > 0.75)
        address_matches = queryset.condition_filer(lambda obj: match_address(obj.address, search_term) > 0.75)

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
                reverse("admin:shop_app_producer_changelist") +
                "?" +
                urlencode({"id": producer.id})
        )

        return format_html('<b><a href="{}">{}</a></b>', link, producer)

    def get_providers_as_link(self, obj):
        providers = obj.providers.all()
        providers_id = ','.join([str(provider.id) for provider in providers])

        link = (
                reverse("admin:shop_app_provider_changelist") +
                "?" +
                urlencode({"id__in": providers_id})
        )

        few_providers = obj.get_few_providers()

        return format_html('<a href="{}">{}</a>', link, few_providers)

    get_producer_as_link.short_description = "Producer"
    get_providers_as_link.short_description = "Providers"


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):

    list_display = ('date', 'product_name', 'count')
    ordering = ('date', 'product_name', 'count')
    list_filter = (('date', DateFieldListFilter), ('product_name', MultiSelectFilter))

    search_fields = ('product_name',)

    def get_search_results(self, request, queryset, search_term):
        date_matches = queryset.condition_filer(lambda obj: match_date(obj.date, search_term) > 0.75)

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
    fields = ('avatar', 'phone', 'address')

    verbose_name_plural = 'Profile'

    # This ensures that inlines fields are required when creating a user.
    min_num = 1
    can_delete = False

    classes = ('no-upper', 'no-title')


@admin.override(User)
class UserProfileAdmin(UserFieldsetsInlineMixin, UserAdmin):
    class Media:
        css = {
            'all': ('css/admin_inline_style.css',)
        }

    inlines = (ProfileInline,)

    list_display = ('username', 'get_avatar_as_html_image', 'email', 'first_name', 'last_name',
                    'get_address', 'get_phone')

    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_search_results(self, request, queryset, search_term):
        check_high_phone_match = lambda obj: match_phone_number(obj.profile.phone, search_term) > 0.75
        check_high_address_match = lambda obj: match_address(obj.profile.address, search_term) > 0.85

        phone_matches = queryset.condition_filer(check_high_phone_match)
        address_matches = queryset.condition_filer(check_high_address_match)

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
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
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
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        })
    )

    readonly_fields = ('last_login', 'date_joined')

    def get_phone(self, obj):
        return obj.profile.phone

    def get_address(self, obj):
        return obj.profile.address

    def get_avatar_as_html_image(self, obj):
        return mark_safe(f'<img src = "{obj.profile.avatar.url}" width = "65"/>')

    get_phone.short_description = "Phone"
    get_address.short_description = "Address"
    get_avatar_as_html_image.short_description = "Avatar"

    list_per_page = 20
