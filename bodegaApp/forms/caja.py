from django import forms
from bodegaApp.models import Caja, Locker

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['nameTag', 'activo', 'adjunto', 'locker']
        widgets = {
            'nameTag': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
            'adjunto': forms.Select(attrs={'class': 'form-control'}),
            'locker': forms.Select(attrs={'class': 'form-control'}),
        }

class CajaMover(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['locker']

    locker = forms.ModelChoiceField(
        queryset=Locker.objects.all(),
        
        required=True,    
        widget=forms.Select(attrs={'class': 'form-control'})
    )