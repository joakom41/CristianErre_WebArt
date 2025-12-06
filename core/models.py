from django.db import models

# Modelo existente: Banner
class Banner(models.Model):
    titulo = models.CharField(max_length=100, default="Slide de Carrusel")
    imagen = models.ImageField(upload_to='banners/', verbose_name="Imagen del Banner")
    orden = models.IntegerField(default=0, verbose_name="Orden de aparición")
    
    class Meta:
        verbose_name = "Slide de Banner"
        verbose_name_plural = "Slides de Banner"
        ordering = ['orden']
        
    def __str__(self):
        return f"Banner {self.orden}: {self.titulo}"

# Modelo de Contacto 
class Contacto(models.Model):
    """Modelo para guardar mensajes de contacto recibidos."""
    
    # Tipos de consulta disponibles
    TIPO_CONSULTA_CHOICES = [
        ('CONSULTA', 'Consulta General'),
        ('ENCARGO', 'Encargo de Obra'),
        ('MURAL', 'Cotización de Muralismo'),
        ('DISPONIBILIDAD', 'Consultar Disponibilidad'),
        ('COTIZACION', 'Solicitar Cotización'),
        ('OTRO', 'Otro'),
    ]
    
    # Campos principales
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    asunto = models.CharField(
        max_length=20, 
        choices=TIPO_CONSULTA_CHOICES,
        default='CONSULTA',
        verbose_name="Tipo de Consulta"
    )
    mensaje = models.TextField(verbose_name="Mensaje")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    
    # Campos para compatibilidad con Funcionalidad 5 (Cotizaciones)
    obra_id = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name="ID de Obra",
        help_text="ID de la obra consultada (si aplica)"
    )
    obra_nombre = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nombre de la Obra",
        help_text="Nombre de la obra consultada (si aplica)"
    )
    
    # Campos para gestión de mensajes por el admin
    respondido = models.BooleanField(default=False, verbose_name="Respondido")
    archivado = models.BooleanField(default=False, verbose_name="Archivado")
    respuesta = models.TextField(blank=True, null=True, verbose_name="Respuesta del Admin")
    fecha_respuesta = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Respuesta")

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['-fecha_envio']),
            models.Index(fields=['obra_id']),
            models.Index(fields=['asunto']),
        ]

    def __str__(self):
        if self.obra_nombre:
            return f"Consulta sobre '{self.obra_nombre}' de {self.nombre}"
        return f"Mensaje de {self.nombre} - {self.get_asunto_display()}"
    
    def es_consulta_obra(self):
        """Verifica si esta consulta es sobre una obra específica."""
        return self.obra_id is not None and self.obra_nombre
    
    @property
    def tipo_consulta_display(self):
        """Retorna el nombre legible del tipo de consulta."""
        return self.get_asunto_display()