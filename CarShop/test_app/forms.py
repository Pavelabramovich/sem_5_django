from .models import Category, Producer, Provider, Product, Buy
from django import forms
from .validators import is_address, is_phone_number


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = '__all__'

    def clean(self):
        forms.ModelForm.clean(self)

        error_dict = {}

        phone = self.cleaned_data.get('phone')
        if not is_phone_number(phone):
            error_dict['phone'] = ["Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX"]

        address = self.cleaned_data.get('address')
        if not is_address(address):
            error_dict['address'] = ["Address is incorrect. It must consist of words, numbers and codes"]

        if error_dict:
            raise forms.ValidationError(error_dict)

        return self.cleaned_data


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

    def clean(self):
        forms.ModelForm.clean(self)

        error_dict = {}

        phone = self.cleaned_data.get('phone')
        if not is_phone_number(phone):
            error_dict['phone'] = ["Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX"]

        address = self.cleaned_data.get('address')
        if not is_address(address):
            error_dict['address'] = ["Address is incorrect. It must consist of words, numbers and codes"]

        if error_dict:
            raise forms.ValidationError(error_dict)

        return self.cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        forms.ModelForm.clean(self)

        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError({'price': ["Price must be positive"]})

        return self.cleaned_data


class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = '__all__'

    def clean(self):
        forms.ModelForm.clean(self)

        error_dict = {}

        count = self.cleaned_data.get('count')
        if count <= 0:
            error_dict['count'] = ["Count must be positive"]

        product_name = self.cleaned_data.get('product_name')
        products = Product.objects.all()

        filtered = filter(lambda p: p.name == product_name, products)

        if len(list(filtered)) == 0:
            raise forms.ValidationError("No products with this name")

        return self.cleaned_data
