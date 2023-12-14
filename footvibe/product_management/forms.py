from django import forms
from .models import Product, ProductVariant,Category, Brand


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_catg', 'product_brand', 'product_description']


class ProductVariantForm(forms.ModelForm):

    class Meta:
        model = ProductVariant
        fields = ['product', 'sku_id', 'attribute_value', 'max_price', 'sale_price', 'stock']


        widgets = {
            'attribute_value': forms.Select(attrs={'class': 'form-control', 'value': 'attribute_value'}),
            }