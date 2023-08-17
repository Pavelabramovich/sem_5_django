from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField

from apps.core.form_tools import LabelOnlyWidget
from .models import Product
from .validators import (
    validate_provider,
    validate_phone_number,
    validate_address,
    is_valid
)


class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=65, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=64, validators=[validate_phone_number],
                            help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = forms.CharField(max_length=64, validators=[validate_address])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class ProviderChangeForm(UserChangeForm):

    products = forms.ModelMultipleChoiceField(
        Product.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Products', False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['products'] = self.instance.products.values_list('pk', flat=True)

            products_field = self.fields['products']

            if not is_valid(validate_provider, self.instance):
                products_field.widget = LabelOnlyWidget()
                products_field.disabled = True

                products_field.label = """
                This user does not have provider permissions. 
                To grant provider permissions to a user, add the user to the Providers group and save.
                """

    def save(self, *args, **kwargs):
        instance = super(ProviderChangeForm, self).save(*args, **kwargs)
        if instance.pk:
            instance.products.clear()
            instance.products.add(*self.cleaned_data['products'])
        return instance
