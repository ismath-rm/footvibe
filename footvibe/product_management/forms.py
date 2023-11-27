from django import forms
from .models import Product, Category, Brand

class CreateProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['product_name','product_catg', 'product_brand', 'product_description']
