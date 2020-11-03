from django import forms

from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'title',
            'company',
            'date',
            'link',
        )
        widgets = {
            'title': forms.TextInput,
            'company': forms.TextInput,
            'date': forms.TextInput,
        }