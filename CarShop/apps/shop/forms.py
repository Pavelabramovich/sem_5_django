from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField

from apps.core.form_tools import LabelOnlyWidget
from django.forms import ModelForm, Textarea

from .models import Product, Provider, Profile, News
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


class UserProfileCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=64, validators=[validate_phone_number],
                            help_text="Enter a phone in format +375 (29) XXX-XX-XX")

    address = forms.CharField(max_length=64, validators=[validate_address])

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)

        if user.pk:
            phone = self.cleaned_data['phone']
            address = self.cleaned_data['address']

            Profile.objects.create(
                user=user,
                phone=phone,
                address=address
            )

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class RegistrationForm(UserProfileCreationForm):
    terms_of_service_accepted = forms.BooleanField(
        required=False,
        label="Provider status",
        help_text="Determines whether the user can provide products."
    )

    def clean(self):
        super().clean()

        terms_of_service_accepted = self.cleaned_data.get('terms_of_service_accepted')

        print(terms_of_service_accepted)

        if not terms_of_service_accepted:
            self._errors['terms_of_service_accepted'] = self.error_class([
                'You must accept all terms of the user agreement.'
            ])

        return self.cleaned_data


class UserAsProviderChangeForm(UserChangeForm):
    products = forms.ModelMultipleChoiceField(
        Product.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Products', False),
        required=False,
    )

    is_provider = forms.BooleanField(
        required=False,
        label="Provider status",
        help_text="Determines whether the user can provide products."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.provider = Provider.objects.filter(user_ptr_id=self.instance.id).first()

            if self.provider:
                self.initial['is_provider'] = True
                self.initial['products'] = self.provider.products.values_list('pk', flat=True)
            else:
                self.initial['is_provider'] = False
                products_field = self.fields['products']

                products_field.widget = LabelOnlyWidget()
                products_field.disabled = True

                products_field.label = """
                This user is not provider. 
                To grant provider permissions to a user, set his provider status and save.
                """

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        if instance.pk:
            is_provider = self.cleaned_data['is_provider']

            if self.provider:
                if is_provider:
                    self.provider.products.clear()
                    self.provider.products.add(*self.cleaned_data['products'])
                else:
                    # Downcast
                    self.provider.delete(keep_parents=True)

            elif is_provider:
                # Upcast
                provider = Provider(pk=self.instance.pk)
                provider.__dict__.update(self.instance.__dict__)
                provider.save()

        return instance


class NewsModelForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

