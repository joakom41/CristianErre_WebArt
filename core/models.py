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
    nombre = models.CharField(max_length=100, verbose_name="Tu Nombre")
    email = models.EmailField(verbose_name="Tu Correo Electrónico")
    asunto = models.CharField(max_length=150, verbose_name="Asunto del Mensaje")
    mensaje = models.TextField(verbose_name="Mensaje")
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    # Campos para gestión de mensajes por el admin
    respondido = models.BooleanField(default=False, verbose_name="Respondido")
    archivado = models.BooleanField(default=False, verbose_name="Archivado")
    respuesta = models.TextField(blank=True, null=True, verbose_name="Respuesta del Admin")
    fecha_respuesta = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Respuesta")

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.asunto}"