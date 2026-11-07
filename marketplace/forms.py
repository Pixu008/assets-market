from django import forms
from .models import Recurso3D

class Recurso3DForm(forms.ModelForm):
    class Meta:
        model = Recurso3D
        # Campos que aparecerán en el formulario (excluimos 'vigente' porque por defecto es True)
        fields = ['categoria', 'codigo_slug', 'titulo', 'descripcion', 'precio_clp', 'estado', 'imagen_preview', 'archivo_zip']
        
        # Inyectar clases de Bootstrap 5 a los inputs
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'codigo_slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej-textura-rindo'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio_clp': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen_preview': forms.FileInput(attrs={'class': 'form-control'}),
            'archivo_zip': forms.FileInput(attrs={'class': 'form-control'}),
        }

    # Validación clean_() obligatoria para el precio (no negativo)
    def clean_precio_clp(self):
        precio = self.cleaned_data.get('precio_clp')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio del asset no puede ser negativo.")
        return precio

    # Validación clean_() obligatoria para identificador único
    def clean_codigo_slug(self):
        codigo = self.cleaned_data.get('codigo_slug')
        # Verificar si ya existe otro asset con ese mismo código
        if Recurso3D.objects.filter(codigo_slug=codigo).exists():
            raise forms.ValidationError("Ya existe un asset con este código. Elige uno diferente.")
        return codigo