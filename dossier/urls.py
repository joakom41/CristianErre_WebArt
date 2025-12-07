from django.urls import path
from . import views

app_name = 'dossier'

urlpatterns = [
    path('crear/', views.crear_dossier, name='crear_dossier'),
    path('generar/<int:dossier_id>/', views.generar_pdf, name='generar_pdf'),
    path('artista/', views.dossier_artista_readonly, name='dossier_artista_readonly'),
    path('artista/pdf/', views.dossier_artista_pdf, name='dossier_artista_pdf'),
    path('artista/generar_pdf/', views.generar_pdf_bloqueado, name='generar_pdf_bloqueado'),
]
