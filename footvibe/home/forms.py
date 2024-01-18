from django import forms
from django.forms import ModelForm
from .models import AddressBook,HomeMainSlide

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressBook
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'country', 'state', 'city', 'pincode']


class HomeMainSliderForm(ModelForm):
    class Meta:
        model = HomeMainSlide
        fields = '__all__'

        widgets = {
            'heading':forms.TextInput(attrs={'class':'form-control'}),
            'subheading':forms.TextInput(attrs={'class':'form-control'}),
            

        }