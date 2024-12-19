from django import forms
from bodegaApp.models import Adjunto

class AdjuntoForm(forms.ModelForm):
    class Meta:
        model = Adjunto
        fields = ['adjunto', 'nombre', 'tipo']
        widgets = {
            'adjunto': forms.FileInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }

