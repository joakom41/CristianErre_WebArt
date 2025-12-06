from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Row, Column
from .models import Contacto


# Estilos base reutilizables
ESTILO_INPUT = 'w-full border border-stone-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-stone-400 focus:border-transparent transition-all duration-300 text-stone-900 placeholder-stone-400'
ESTILO_SELECT = 'w-full border border-stone-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-stone-400 focus:border-transparent transition-all duration-300 text-stone-900 bg-white'
ESTILO_TEXTAREA = 'w-full border border-stone-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-stone-400 focus:border-transparent transition-all duration-300 text-stone-900 placeholder-stone-400 resize-none'


class ContactoForm(forms.ModelForm):
    """
    Formulario de contacto optimizado para la Funcionalidad 5.
    Soporta pre-llenado desde consultas de obras específicas.
    """
    
    # Campo oculto para almacenar la referencia a la obra
    obra_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        help_text="ID de la obra (se pre-llena desde URL)"
    )

    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'asunto', 'mensaje', 'obra_id', 'obra_nombre']
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'asunto': 'Tipo de Consulta',
            'mensaje': 'Mensaje',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': ESTILO_INPUT,
                'placeholder': 'Tu nombre completo',
                'maxlength': '100',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': ESTILO_INPUT,
                'placeholder': 'tu@email.com',
                'autocomplete': 'email',
            }),
            'asunto': forms.Select(attrs={
                'class': ESTILO_SELECT,
                'aria-label': 'Tipo de consulta',
            }),
            'mensaje': forms.Textarea(attrs={
                'class': ESTILO_TEXTAREA,
                'rows': '6',
                'placeholder': 'Cuéntanos sobre tu proyecto o consulta...',
                'minlength': '10',
                'maxlength': '5000',
            }),
            'obra_nombre': forms.HiddenInput(),
        }

    def __init__(self, *args, obra_nombre=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Eliminar ayuda del modelo si la hay
        for field in self.fields:
            self.fields[field].help_text = None
        
        # Configuración de Crispy Forms para layout responsive
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.form_tag = True
        self.helper.use_custom_control = False
        
        # Guardar obra_nombre para usar en clean() si es necesario
        self.obra_nombre = obra_nombre
        
        # Layout responsive
        self.helper.layout = Layout(
            Field('obra_id'),  # Campo oculto
            Field('obra_nombre'),  # Campo oculto
            
            Row(
                Column('nombre', css_class='col-12'),
                css_class='row'
            ),
            Row(
                Column('email', css_class='col-12'),
                css_class='row'
            ),
            Row(
                Column('asunto', css_class='col-12'),
                css_class='row'
            ),
            Row(
                Column('mensaje', css_class='col-12'),
                css_class='row'
            ),
            
            # Botón de envío
            HTML(
                '<button type="submit" '
                'class="w-full bg-stone-900 hover:bg-stone-800 active:bg-stone-950 '
                'text-white font-medium py-3 px-4 rounded-xl transition-all duration-300 '
                'mt-6 focus:outline-none focus:ring-2 focus:ring-stone-400 '
                'disabled:opacity-50 disabled:cursor-not-allowed" '
                'aria-label="Enviar solicitud">'
                'Enviar Solicitud'
                '</button>'
            )
        )

    def clean_email(self):
        """Valida que el email sea único en un período de tiempo."""
        email = self.cleaned_data.get('email')
        
        if email:
            # Verificar si hay demasiados mensajes del mismo email en las últimas 24 horas
            from django.utils import timezone
            from datetime import timedelta
            
            hace_24h = timezone.now() - timedelta(hours=24)
            mensajes_recientes = Contacto.objects.filter(
                email=email,
                fecha_envio__gte=hace_24h
            ).count()
            
            if mensajes_recientes >= 5:
                raise forms.ValidationError(
                    "Has enviado demasiados mensajes en las últimas 24 horas. "
                    "Por favor, intenta más tarde."
                )
        
        return email

    def clean_mensaje(self):
        """Valida que el mensaje tenga contenido útil."""
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        
        if len(mensaje) < 10:
            raise forms.ValidationError(
                "El mensaje debe tener al menos 10 caracteres."
            )
        
        if len(mensaje) > 5000:
            raise forms.ValidationError(
                "El mensaje no puede exceder 5000 caracteres."
            )
        
        return mensaje

    def clean(self):
        """Validaciones adicionales a nivel de formulario."""
        cleaned_data = super().clean()
        
        # Si obra_id está presente, validar que sea un número
        obra_id = cleaned_data.get('obra_id')
        if obra_id:
            try:
                int(obra_id)
            except (ValueError, TypeError):
                self.add_error('obra_id', 'ID de obra inválido.')
        
        return cleaned_data