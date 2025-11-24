# catalogo/urls.py

from django.urls import path
from . import views

# Defino el nombre de la aplicación 
app_name = 'catalogo' 

urlpatterns = [
    # Mapeo la URL base del catálogo a mi vista con filtros (R4)
    path('', views.lista_obras, name='lista_obras'), 
]