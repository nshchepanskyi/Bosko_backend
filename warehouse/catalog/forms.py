from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity')
        labels = {
            'name': 'Назва',
            'description': 'Опис',
            'price': 'Ціна (грн)',
            'quantity': 'Кількість',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
        }