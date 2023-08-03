from .models import Category, Producer, Provider, Product, Buy, Profile
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = '__all__'


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = '__all__'