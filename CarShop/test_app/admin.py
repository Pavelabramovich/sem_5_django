from django.contrib import admin
from .models import ProductType, Provider, Producer, Product, Bye
from django import forms
from .validators import is_address, is_phone_number


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

    def clean(self):

        phone = self.cleaned_data.get('phone')
        if not is_phone_number(phone):
            raise forms.ValidationError("Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX")

        address = self.cleaned_data.get('address')
        if not is_address(address):
            raise forms.ValidationError("Address is incorrect. It must consist of words, numbers and codes")

        return self.cleaned_data


class ProviderAdmin(admin.ModelAdmin):
    form = ProviderForm
    list_display = ('name', 'phone', 'address')


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = '__all__'

    def clean(self):

        phone = self.cleaned_data.get('phone')
        if not is_phone_number(phone):
            raise forms.ValidationError("Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX")

        address = self.cleaned_data.get('address')
        if not is_address(address):
            raise forms.ValidationError("Address is incorrect. It must consist of words, numbers and codes")

        return self.cleaned_data


class ProducerAdmin(admin.ModelAdmin):
    form = ProducerForm
    list_display = ('name', 'phone', 'address')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price must be positive")

        return self.cleaned_data


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'product_type', 'price', 'display_producer', 'display_short_providers')

    fieldsets = (
        (None, {
            'fields': ('name', 'product_type', 'price')
        }),
        ('Detailed information', {
            'fields': ('article', 'producer', 'providers')
        }),
    )


class ByeForm(forms.ModelForm):
    class Meta:
        model = Bye
        fields = '__all__'

    def clean(self):
        count = self.cleaned_data.get('count')
        if count <= 0:
            raise forms.ValidationError("Count must be positive")

        product_name = self.cleaned_data.get('product_name')
        products = Product.objects.all()

        filtered = filter(lambda p: p.name == product_name, products)

        if len(list(filtered)) == 0:
            raise forms.ValidationError("No products with this name")

        return self.cleaned_data


class ByeAdmin(admin.ModelAdmin):
    form = ByeForm
    list_display = ('date', 'product_name', 'count')


admin.site.register(ProductType)

admin.site.register(Provider, ProviderAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bye, ByeAdmin)
