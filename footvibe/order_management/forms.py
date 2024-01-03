from .models import Order
from django import forms

class OrderForm(forms.ModelForm):
     class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})  # Apply attrs to the Select widget
        }