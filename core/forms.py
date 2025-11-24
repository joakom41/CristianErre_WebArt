from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Contacto


# Opciones para el campo 'asunto' (mapeo desde el antiguo select 'tipo_consulta')
TIPO_CONSULTA_CHOICES = [
    ('general', 'Consulta General'),
    ('encargo', 'Encargo de Obra'),
    ('mural', 'Cotización de Muralismo'),
]


class ContactoForm(forms.ModelForm):
    # Sobrescribo el campo 'asunto' para mostrar un select con las opciones deseadas
    asunto = forms.ChoiceField(
        choices=TIPO_CONSULTA_CHOICES,
        label='Tipo de Consulta',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'mensaje': 'Mensaje',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuración básica de Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Agrego un botón de submit consistente con el diseño (se puede sobreescribir en la plantilla)
        self.helper.add_input(Submit('submit', 'Enviar Solicitud', css_class='btn btn-lg w-100 text-white'))
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Contacto

class ContactoForm(forms.ModelForm):
    """Formulario de contacto basado en el modelo Contacto, usando Crispy Forms."""

    class Meta:
        model = Contacto
        # Mapea los campos del modelo Contacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de Crispy Forms 
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Define la estructura visual con los campos y el botón de envío
        self.helper.layout = Layout(
            'nombre',
            'email',
            'asunto',
            'mensaje',
            # Botón de envío que aplica el estilo de Bootstrap 5
            Submit('submit', 'Enviar Solicitud', css_class='btn-dark btn-lg w-100 mt-3')
        )