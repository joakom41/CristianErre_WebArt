from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Dossier, DossierObra

class DossierObraInline(admin.TabularInline):
    model = DossierObra
    extra = 0
    fields = ('obra', 'orden')
    readonly_fields = ('obra', 'orden')

@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ('nombre_artista', 'fecha_generacion', 'cantidad_obras', 'ver_pdf')
    list_filter = ('fecha_generacion',)
    search_fields = ('nombre_artista',)
    inlines = [DossierObraInline]
    
    def cantidad_obras(self, obj):
        return obj.obras.count()
    cantidad_obras.short_description = 'Obras'
    
    def ver_pdf(self, obj):
        url = reverse('dossier:generar_pdf', args=[obj.id])
        return format_html('<a class="button" href="{}">📄 Descargar PDF</a>', url)
    ver_pdf.short_description = 'Acción'
    
    # Ocultar el botón "Agregar" porque usaremos la vista custom
    def has_add_permission(self, request):
        return False