from .models import Category, Producer, Provider, Product, Buy, Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .validators import \
    validate_phone_number, \
    validate_address


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
