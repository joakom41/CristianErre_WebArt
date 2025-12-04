from django.urls import path
from . import views

app_name = 'dossier'

urlpatterns = [
    path('crear/', views.crear_dossier, name='crear_dossier'),
    path('generar/<int:dossier_id>/', views.generar_pdf, name='generar_pdf'),
]
