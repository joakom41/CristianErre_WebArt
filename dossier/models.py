from django.db import models
from catalogo.models import Obra

class Dossier(models.Model):
    # Información del artista (no se guarda, solo temporal)
    nombre_artista = models.CharField(max_length=200, verbose_name="Nombre del Artista")
    bio_artista = models.TextField(blank=True, verbose_name="Biografía (Opcional)")
    foto_artista_url = models.URLField(max_length=500, verbose_name="URL Foto del Artista")
    
    # Relación con obras seleccionadas (máximo 20)
    obras = models.ManyToManyField(
        Obra,
        through='DossierObra',
        related_name='dossiers',
        verbose_name="Obras Seleccionadas"
    )
    
    # Metadatos
    fecha_generacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Generación")
    
    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"Dossier - {self.nombre_artista} ({self.fecha_generacion.strftime('%d/%m/%Y')})"


class DossierObra(models.Model):
    """Modelo intermedio para mantener el orden de las obras en el dossier"""
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden en el Dossier")
    
    class Meta:
        ordering = ['orden']
        unique_together = ['dossier', 'obra', 'orden']