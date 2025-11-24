from django.contrib import admin
# Importo todos los modelos que necesito registrar
from .models import Artista, Estilo, Obra

# ----------------------------------------------------
# 1. Administración del Modelo OBRA (Personalización de 6 Parámetros)
# ----------------------------------------------------
class ObraAdmin(admin.ModelAdmin):
    # Función auxiliar para mostrar los Estilos de forma legible en la lista
    def get_estilos(self, obj):
        # Muestro una lista de los nombres de estilos separados por coma
        return ", ".join([estilo.nombre for estilo in obj.estilos.all()])
    # Doy un nombre de columna legible al método
    get_estilos.short_description = 'Estilos' 
    
    # 1. list_display: Campos visibles en la lista (Obligatorio)
    list_display = ('titulo', 'artista', 'get_estilos', 'estado', 'creado',)
    
    # 2. list_filter: Filtros laterales (Cumplo con un parámetro clave)
    list_filter = ('artista', 'estado', 'estilos',)
    
    # 3. search_fields: Campos donde puedo buscar (barra de búsqueda)
    search_fields = ('titulo', 'descripcion', 'artista__nombre',) 
    
    # 4. list_editable: Permite cambiar el estado de venta directamente en la lista
    list_editable = ('estado',)
    
    # 5. readonly_fields: Campos que no puedo modificar después de la creación
    readonly_fields = ('creado', 'actualizado',)
    
    # 6. filter_horizontal: Widget mejorado para ManyToManyField
    filter_horizontal = ('estilos',) 
    
# ----------------------------------------------------
# 2. Registro de Modelos en el Admin
# ----------------------------------------------------

# Registro el modelo Obra con su personalización
admin.site.register(Obra, ObraAdmin)

# Registro los modelos Artista y Estilo (¡Esto hace que aparezcan en el panel!)
admin.site.register(Artista)
admin.site.register(Estilo)