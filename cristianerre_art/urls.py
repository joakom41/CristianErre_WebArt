from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Importo mi vista del 404
from core.views import error_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de la aplicación principal (core)
    path('', include('core.urls')), 
    
    # URLs del Catálogo (Obras de Arte)
    # Usamos un namespace 'catalogo' para evitar conflictos (ej: catalogo:lista_obras)
    path('catalogo/', include('catalogo.urls')), 
]

# Configuración de URLs para archivos MEDIA y STATIC
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Handler 404 (Requisito 3)
# Uso el string path en lugar de la referencia directa para evitar problemas de importación circular
handler404 = 'core.views.error_404_view'