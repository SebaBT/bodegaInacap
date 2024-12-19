from django import forms
from bodegaApp.models import Locker

class LockerForm(forms.ModelForm):
    class Meta:
        model = Locker
        fields = ['nameTag', 'comentario', 'adjunto']
        widgets = {
            'nameTag': forms.TextInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'cols': '50', 'rows': '5'}),
            'adjunto': forms.Select(attrs={'class': 'form-control'}),
        }
