from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.home_view, name='home'), 
    path('bio/', views.bio_view, name='bio'), 
    path('contacto/', views.contacto_view, name='contacto'), 
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Panel de Administración
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    
    # Gestión de Obras
    path('admin-panel/obras/', views.admin_obras_view, name='admin_obras'),
    path('admin-panel/obras/nueva/', views.admin_obra_create_view, name='admin_obra_create'),
    path('admin-panel/obras/<int:obra_id>/editar/', views.admin_obra_edit_view, name='admin_obra_edit'),
    path('admin-panel/obras/<int:obra_id>/eliminar/', views.admin_obra_delete_view, name='admin_obra_delete'),
    
    # Gestión de Mensajes
    path('admin-panel/mensajes/', views.admin_mensajes_view, name='admin_mensajes'),
    path('admin-panel/mensajes/<int:mensaje_id>/', views.admin_mensaje_detail_view, name='admin_mensaje_detail'),
    path('admin-panel/mensajes/<int:mensaje_id>/responder/', views.admin_mensaje_respond_view, name='admin_mensaje_respond'),
    path('admin-panel/mensajes/<int:mensaje_id>/archivar/', views.admin_mensaje_archive_view, name='admin_mensaje_archive'),
]