from django import forms
from bodegaApp.models import Prestamo
from bodegaApp.models.inventario import Insumo
from django.db.models import Q


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['solicitante', 'insumo', 'adjunto', 'ubicacion', 'notas', 'estado']
        widgets = {
            'solicitante': forms.Select(attrs={'class': 'form-control'}),
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'adjunto': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control' , 'cols': '20', 'rows': '4'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            criterion1 = Q(activo=True)
            criterion2 = Q(id=self.instance.insumo.id)
            self.fields['insumo'].queryset = Insumo.objects.filter(criterion1 | criterion2)
            self.fields['insumo'].initial = self.instance.insumo
        else:
            self.fields['insumo'].queryset = Insumo.objects.filter(activo=True)