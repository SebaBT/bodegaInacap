from django import forms
from bodegaApp.models import Insumo, Caja, Locker

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'activo', 'adjunto', 'categoria', 'locker', 'caja']  # Updated fields
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'cols': '20', 'rows': '2'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Widget for BooleanField
            'adjunto': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'locker': forms.Select(attrs={'class': 'form-control'}),
            'caja': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        locker = cleaned_data.get("locker")

        if not locker:
            msg = "Un insumo debe estar en un locker."
            self.add_error("locker", msg)

class InsumoMover(forms.ModelForm):
    locker = forms.ModelChoiceField(
        queryset=Locker.objects.all(),
        empty_label="No Locker",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'locker-select'})
    )
    caja = forms.ModelChoiceField(
        queryset=Caja.objects.none(),  
        empty_label="No Caja",  
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'caja-select'}) 
    )

    class Meta:
        model = Insumo
        fields = ['locker', 'caja']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.locker: 
            self.fields['caja'].queryset = Caja.objects.filter(lockerID=self.instance.locker)