from django.forms import ModelMultipleChoiceField
from django.contrib.auth.models import User, Permission
from django.db.models import Q, QuerySet
from .models import Category, Product, Buy, Profile
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .queryset_condition_filter import queryset_condition_filter
from .validators import validate_provider, validate_phone_number, validate_address, to_condition
from .m2m_validation import m2m_validation


QuerySet.condition_filer = queryset_condition_filter


@m2m_validation({'providers': (validate_provider,)})
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    providers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().condition_filer(to_condition(validate_provider)),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            initial_providers = self.instance.providers.values_list('pk', flat=True)
            self.initial['providers'] = initial_providers

    def save(self, *args, **kwargs):
        kwargs['commit'] = True
        return super().save(*args, **kwargs)

    def save_m2m(self):
        self.instance.providers.clear()
        self.instance.providers.add(*self.cleaned_data['providers'])

    def clean(self):
        super().clean()

        providers = self.cleaned_data.get('providers')
        providers_error_list = []

        for provider in providers:
            try:
                validate_provider(provider)
            except forms.ValidationError as error:
                providers_error_list.append(error.message)

        if providers_error_list:
            raise forms.ValidationError({'providers': providers_error_list})

        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=64, validators=[validate_phone_number],
                            help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = forms.CharField(max_length=64, validators=[validate_address])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
