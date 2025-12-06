from django.contrib import admin
from .models import Banner, Contacto


class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'imagen',)
    list_editable = ('orden',)  # Facilita el control del orden


class ContactoAdmin(admin.ModelAdmin):
    """Admin mejorado para gestionar mensajes de contacto con Funcionalidad 5."""
    
    list_display = (
        'nombre', 
        'tipo_consulta_display', 
        'obra_nombre_short',
        'email', 
        'fecha_envio_short',
        'respondido_icon',
        'archivado_icon',
    )
    
    list_filter = (
        'asunto', 
        'respondido', 
        'archivado',
        'fecha_envio',
        'obra_id',
    )
    
    search_fields = (
        'nombre', 
        'email', 
        'obra_nombre',
        'mensaje',
        'asunto',
    )
    
    readonly_fields = (
        'fecha_envio',
        'fecha_respuesta',
        'es_consulta_obra',
        'mensaje_preview',
    )
    
    fieldsets = (
        ('Información del Contacto', {
            'fields': ('nombre', 'email', 'fecha_envio')
        }),
        ('Detalles de la Consulta', {
            'fields': ('asunto', 'mensaje', 'mensaje_preview')
        }),
        ('Información de Obra (Funcionalidad 5)', {
            'fields': ('obra_id', 'obra_nombre', 'es_consulta_obra'),
            'classes': ('collapse',),
            'description': 'Información de la obra consultada (si aplica).'
        }),
        ('Respuesta del Admin', {
            'fields': ('respondido', 'respuesta', 'fecha_respuesta'),
            'classes': ('collapse',),
        }),
        ('Gestión', {
            'fields': ('archivado',),
        }),
    )
    
    actions = [
        'marcar_como_respondido',
        'marcar_como_no_respondido',
        'archivar_mensajes',
        'desarchivar_mensajes',
    ]
    
    date_hierarchy = 'fecha_envio'
    ordering = ('-fecha_envio',)
    
    def tipo_consulta_display(self, obj):
        """Muestra el tipo de consulta de forma legible."""
        return obj.get_asunto_display()
    tipo_consulta_display.short_description = 'Tipo de Consulta'
    
    def obra_nombre_short(self, obj):
        """Muestra el nombre de la obra truncado."""
        if obj.obra_nombre:
            return obj.obra_nombre[:30] + '...' if len(obj.obra_nombre) > 30 else obj.obra_nombre
        return '—'
    obra_nombre_short.short_description = 'Obra'
    
    def fecha_envio_short(self, obj):
        """Muestra la fecha en formato corto."""
        return obj.fecha_envio.strftime('%d/%m/%y %H:%M')
    fecha_envio_short.short_description = 'Fecha'
    
    def respondido_icon(self, obj):
        """Muestra un ícono indicando si fue respondido."""
        if obj.respondido:
            return '✅ Sí'
        return '❌ No'
    respondido_icon.short_description = 'Respondido'
    respondido_icon.admin_order_field = 'respondido'
    
    def archivado_icon(self, obj):
        """Muestra un ícono indicando si está archivado."""
        if obj.archivado:
            return '📦 Archivado'
        return '📂 Activo'
    archivado_icon.short_description = 'Estado'
    archivado_icon.admin_order_field = 'archivado'
    
    def es_consulta_obra(self, obj):
        """Muestra si la consulta es sobre una obra."""
        return obj.es_consulta_obra()
    es_consulta_obra.short_description = 'Es Consulta de Obra'
    
    def mensaje_preview(self, obj):
        """Muestra una vista previa del mensaje."""
        if len(obj.mensaje) > 100:
            return obj.mensaje[:100] + '...'
        return obj.mensaje
    mensaje_preview.short_description = 'Vista Previa del Mensaje'
    
    def marcar_como_respondido(self, request, queryset):
        """Acción para marcar como respondido."""
        updated = queryset.update(respondido=True)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como respondido.')
    marcar_como_respondido.short_description = 'Marcar como respondido'
    
    def marcar_como_no_respondido(self, request, queryset):
        """Acción para marcar como NO respondido."""
        updated = queryset.update(respondido=False)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como NO respondido.')
    marcar_como_no_respondido.short_description = 'Marcar como NO respondido'
    
    def archivar_mensajes(self, request, queryset):
        """Acción para archivar mensajes."""
        updated = queryset.update(archivado=True)
        self.message_user(request, f'{updated} mensaje(s) archivado(s).')
    archivar_mensajes.short_description = 'Archivar mensajes'
    
    def desarchivar_mensajes(self, request, queryset):
        """Acción para desarchivar mensajes."""
        updated = queryset.update(archivado=False)
        self.message_user(request, f'{updated} mensaje(s) desarchivado(s).')
    desarchivar_mensajes.short_description = 'Desarchivar mensajes'


admin.site.register(Banner, BannerAdmin)
admin.site.register(Contacto, ContactoAdmin)