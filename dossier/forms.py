from django import forms
from django.core.exceptions import ValidationError
from catalogo.models import Obra, Artista
from .models import Dossier

class DossierForm(forms.ModelForm):
    # Campos del artista
    nombre_artista = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
        help_text="Se completará automáticamente con la información del artista"
    )
    bio_artista = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biografía (opcional)'}),
        help_text="Se completará automáticamente con la biografía cargada del artista"
    )
    foto_artista_url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/foto.jpg'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener la información del artista principal (primer artista cargado)
        artista = Artista.objects.first()
        if artista:
            self.fields['nombre_artista'].initial = artista.nombre
            self.fields['bio_artista'].initial = artista.biografia
        
        # Obtener las 10 obras más recientes
        obras_recientes = Obra.objects.all()[:10]
        
        # Crear 10 campos de selección dinámicamente
        for i in range(10):
            field_name = f'obra_{i+1}'
            self.fields[field_name] = forms.ModelChoiceField(
                queryset=Obra.objects.all().order_by('-creado'),
                required=False,
                empty_label="-- Seleccionar obra --",
                widget=forms.Select(attrs={'class': 'form-control obra-selector'}),
                label=f"Obra #{i+1}"
            )
            # Pre-seleccionar si hay obras suficientes
            if i < len(obras_recientes):
                self.fields[field_name].initial = obras_recientes[i].id
    
    def clean(self):
        """Validar que haya biografía cargada del artista"""
        cleaned_data = super().clean()
        bio_artista = cleaned_data.get('bio_artista', '').strip()
        
        # Verificar que la biografía no esté vacía
        if not bio_artista:
            raise ValidationError(
                'Error: No hay una biografía cargada del artista. '
                'Por favor, carga la información "El Artista" desde el panel de administración antes de generar el dossier público.'
            )
        
        return cleaned_data
    
    class Meta:
        model = Dossier
        fields = ['nombre_artista', 'bio_artista', 'foto_artista_url']