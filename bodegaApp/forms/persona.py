from django import forms
from bodegaApp.models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['rut', 'nombre_completo', 'fecha_nacimiento']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # Specify date type
        }