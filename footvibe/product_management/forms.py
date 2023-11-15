from django import forms
from .models import Product, Category, Brand

class CreateProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields =['product_name','product_catg','sku_id','product_brand','max_price','sale_price','product_description','image']