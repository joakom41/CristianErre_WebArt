from django.db import models

# ----------------------------------------------------
# MODELO 1: ARTISTA (Lado 'Uno' en la relación 1:N con Obra)
# ----------------------------------------------------
class Artista(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Artista")
    biografia = models.TextField(verbose_name="Biografía")
    # Pongo blank=True para que el campo sea opcional en el formulario del Admin
    sitio_web = models.URLField(blank=True, verbose_name="Sitio Web")
    
    class Meta:
        verbose_name = "Artista"
        verbose_name_plural = "Artistas"

    def __str__(self):
        return self.nombre


# ----------------------------------------------------
# MODELO 2: ESTILO (Lado 'Muchos' en la relación N:M con Obra)
# ----------------------------------------------------
class Estilo(models.Model):
    # Uso unique=True para evitar estilos duplicados
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Estilo/Técnica") 
    
    class Meta:
        verbose_name = "Estilo o Etiqueta"
        verbose_name_plural = "Estilos y Etiquetas"

    def __str__(self):
        return self.nombre


# ----------------------------------------------------
# MODELO 3: OBRA (Conexiones 1:N y N:M)
# ----------------------------------------------------
class Obra(models.Model):
    # 1. RELACIÓN 1:N (ForeignKey) con Artista:
    # Uso SET_NULL, si borro el artista, este campo queda NULL.
    artista = models.ForeignKey(
        Artista, 
        on_delete=models.SET_NULL,  # Si elimino al artista, este campo se pone a NULL
        null=True,              # Permito NULL en la base de datos
        blank=True,              # Permito que sea opcional en el Admin
        related_name='obras',    
        verbose_name="Artista Creador"
    )

    # 2. RELACIÓN N:M (ManyToManyField) con Estilo:
    estilos = models.ManyToManyField(
        Estilo, 
        related_name='obras_asociadas', 
        verbose_name="Estilos Aplicados"
    )

    # --- Atributos de Contenido ---
    titulo = models.CharField(max_length=200, verbose_name="Título de la Obra")
    
    CATEGORIAS = (
        ('OLEO', 'Óleo sobre Tela'),
        ('ILUSTRACION', 'Ilustración Digital'),
        ('MURALISMO', 'Muralismo / Gran Formato'),
    )
    categoria = models.CharField(
        max_length=20, choices=CATEGORIAS, default='OLEO', verbose_name="Línea de Arte"
    )
    
    descripcion = models.TextField(verbose_name="Descripción Detallada")
    
    ESTADOS = (
        ('DISPONIBLE', 'Disponible para Venta'),
        ('VENDIDO', 'Vendido'),
        ('COTI', 'Sólo Cotización'),
    )
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='DISPONIBLE', verbose_name="Estado de Venta"
    )
    
    # Uso URLField según la necesidad de usar una URL remota
    imagen_url = models.URLField(
        max_length=500, verbose_name="URL Remota de la Imagen"
    )
    
    # --- Atributos de Fecha/Hora ---
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Obra de Arte"
        verbose_name_plural = "Obras de Arte"
        # Ordeno las obras por fecha de creación descendente por defecto
        ordering = ['-creado']
        
    def __str__(self):
        return self.titulo