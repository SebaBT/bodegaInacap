from django import forms
from bodegaApp.models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombreCategoria']
        widgets = {
            'nombreCategoria': forms.TextInput(attrs={'class': 'form-control'}),
        }
