from django import forms
from catalogo.models import Obra
from .models import Dossier

class DossierForm(forms.ModelForm):
    # Campos del artista
    nombre_artista = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'})
    )
    bio_artista = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biografía (opcional)'})
    )
    foto_artista_url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/foto.jpg'})
    )
    
    # Campo dinámico para obras (se manejará con JavaScript)
    obras_seleccionadas = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    class Meta:
        model = Dossier
        fields = ['nombre_artista', 'bio_artista', 'foto_artista_url']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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