from django import forms
from .models import Product, ProductVariant,Category, Brand


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_catg', 'product_brand', 'product_description']


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = [ 'sku_id', 'max_price', 'sale_price', 'stock','thumbnail_image']

        widgets = {
            'attribute_value': forms.Select(attrs={'class': 'form-control'}),
            'max_price': forms.TextInput(attrs={'class': 'form-control'}),
            'sale_price': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
           'thumbnail_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        