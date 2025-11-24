from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Banner
from .forms import ContactoForm
from django.http import HttpResponseNotFound
from django.db import models
from catalogo.models import Obra


# FUNCIÓN AUXILIAR
def get_carousel_context():
    return {'banners': Banner.objects.all().order_by('orden')}


# VISTA HOME (única y correcta)
def home_view(request):
    context = get_carousel_context()

    # Obras históricas: Murales y obras vendidas
    murales = Obra.objects.filter(estilos__nombre__iexact="Mural")
    vendidas = Obra.objects.filter(estado="VENDIDO")
    obras_historicas = (murales | vendidas).distinct().order_by('-creado')[:6]
    
    # Obras recientes disponibles para el catálogo preview (solo 3)
    obras_recientes = Obra.objects.filter(estado='DISPONIBLE').order_by('-creado')[:3]

    context['obras_historicas'] = obras_historicas
    context['obras_recientes'] = obras_recientes

    return render(request, 'core/home.html', context)


# VISTA BIO
def bio_view(request):
    context = get_carousel_context()
    return render(request, 'core/bio.html', context)


# VISTA CONTACTO
def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'¡Gracias {form.cleaned_data["nombre"]}! Su mensaje ha sido enviado con éxito.'
            )
            return redirect('/contacto/')
    else:
        form = ContactoForm()

    context = get_carousel_context()
    context['form'] = form
    return render(request, 'core/contacto.html', context)


# ERROR 404
def error_404_view(request, exception=None):
    context = get_carousel_context()
    return render(request, '404.html', context, status=404)


# ============================================
# VISTAS DE AUTENTICACIÓN
# ============================================
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_view(request):
    """Vista de inicio de sesión"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Buscar usuario por email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name}!')
                # Redirigir al panel admin si es admin, sino a home
                if user.is_staff or user.is_superuser:
                    return redirect('admin_panel')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except User.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese email.')
    
    return render(request, 'core/login.html')


def register_view(request):
    """Vista de registro de nuevos usuarios"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'core/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese email.')
            return render(request, 'core/register.html')
        
        # Crear usuario
        username = email.split('@')[0]  # Usar parte del email como username
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
        return redirect('login')
    
    return render(request, 'core/register.html')


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')


# ============================================
# VISTAS DEL PANEL DE ADMINISTRACIÓN
# ============================================
from .decorators import admin_required
from .models import Contacto
from catalogo.models import Obra, Artista, Estilo
from django.db.models import Count, Q
from django.utils import timezone

@admin_required
def admin_panel_view(request):
    """Dashboard principal del administrador"""
    # Estadísticas
    total_obras = Obra.objects.count()
    obras_disponibles = Obra.objects.filter(estado='DISPONIBLE').count()
    obras_vendidas = Obra.objects.filter(estado='VENDIDO').count()
    mensajes_nuevos = Contacto.objects.filter(respondido=False, archivado=False).count()
    mensajes_total = Contacto.objects.count()
    
    context = {
        'total_obras': total_obras,
        'obras_disponibles': obras_disponibles,
        'obras_vendidas': obras_vendidas,
        'mensajes_nuevos': mensajes_nuevos,
        'mensajes_total': mensajes_total,
    }
    return render(request, 'core/admin_panel.html', context)


@admin_required
def admin_obras_view(request):
    """Lista de todas las obras para gestión"""
    obras = Obra.objects.all().select_related('artista').prefetch_related('estilos')
    context = {'obras': obras}
    return render(request, 'core/admin_obras.html', context)


@admin_required
def admin_obra_create_view(request):
    """Crear nueva obra"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')
        imagen_url = request.POST.get('imagen_url')
        estilos_ids = request.POST.getlist('estilos')
        
        # Crear obra (sin artista, siempre es Cristian Erre)
        obra = Obra.objects.create(
            titulo=titulo,
            categoria=categoria,
            descripcion=descripcion,
            estado=estado,
            imagen_url=imagen_url
        )
        
        # Agregar estilos
        if estilos_ids:
            obra.estilos.set(estilos_ids)
        
        messages.success(request, f'Obra "{titulo}" creada exitosamente.')
        return redirect('admin_obras')
    
    # GET: mostrar formulario
    estilos = Estilo.objects.all()
    context = {
        'estilos': estilos,
        'categorias': Obra.CATEGORIAS,
        'estados': Obra.ESTADOS,
    }
    return render(request, 'core/admin_obra_form.html', context)


@admin_required
def admin_obra_edit_view(request, obra_id):
    """Editar obra existente"""
    from django.shortcuts import get_object_or_404
    obra = get_object_or_404(Obra, id=obra_id)
    
    if request.method == 'POST':
        obra.titulo = request.POST.get('titulo')
        obra.categoria = request.POST.get('categoria')
        obra.descripcion = request.POST.get('descripcion')
        obra.estado = request.POST.get('estado')
        obra.imagen_url = request.POST.get('imagen_url')
        obra.save()
        
        # Actualizar estilos
        estilos_ids = request.POST.getlist('estilos')
        if estilos_ids:
            obra.estilos.set(estilos_ids)
        
        messages.success(request, f'Obra "{obra.titulo}" actualizada exitosamente.')
        return redirect('admin_obras')
    
    # GET: mostrar formulario con datos actuales
    estilos = Estilo.objects.all()
    context = {
        'obra': obra,
        'estilos': estilos,
        'categorias': Obra.CATEGORIAS,
        'estados': Obra.ESTADOS,
        'edit_mode': True,
    }
    return render(request, 'core/admin_obra_form.html', context)


@admin_required
def admin_obra_delete_view(request, obra_id):
    """Eliminar obra"""
    from django.shortcuts import get_object_or_404
    obra = get_object_or_404(Obra, id=obra_id)
    titulo = obra.titulo
    obra.delete()
    messages.success(request, f'Obra "{titulo}" eliminada exitosamente.')
    return redirect('admin_obras')


@admin_required
def admin_mensajes_view(request):
    """Lista de mensajes de contacto"""
    # Filtros
    filtro = request.GET.get('filtro', 'todos')
    
    if filtro == 'nuevos':
        mensajes = Contacto.objects.filter(respondido=False, archivado=False)
    elif filtro == 'respondidos':
        mensajes = Contacto.objects.filter(respondido=True)
    elif filtro == 'archivados':
        mensajes = Contacto.objects.filter(archivado=True)
    else:
        mensajes = Contacto.objects.all()
    
    context = {
        'mensajes': mensajes,
        'filtro_actual': filtro,
    }
    return render(request, 'core/admin_mensajes.html', context)


@admin_required
def admin_mensaje_detail_view(request, mensaje_id):
    """Ver detalle de un mensaje"""
    from django.shortcuts import get_object_or_404
    mensaje = get_object_or_404(Contacto, id=mensaje_id)
    context = {'mensaje': mensaje}
    return render(request, 'core/admin_mensaje_detail.html', context)


@admin_required
def admin_mensaje_respond_view(request, mensaje_id):
    """Responder a un mensaje"""
    from django.shortcuts import get_object_or_404
    mensaje = get_object_or_404(Contacto, id=mensaje_id)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        mensaje.respuesta = respuesta
        mensaje.respondido = True
        mensaje.fecha_respuesta = timezone.now()
        mensaje.save()
        
        messages.success(request, 'Respuesta guardada. Puedes enviar el email manualmente.')
        return redirect('admin_mensajes')
    
    context = {'mensaje': mensaje}
    return render(request, 'core/admin_mensaje_respond.html', context)


@admin_required
def admin_mensaje_archive_view(request, mensaje_id):
    """Archivar un mensaje"""
    from django.shortcuts import get_object_or_404
    mensaje = get_object_or_404(Contacto, id=mensaje_id)
    mensaje.archivado = not mensaje.archivado  # Toggle
    mensaje.save()
    
    estado = 'archivado' if mensaje.archivado else 'desarchivado'
    messages.success(request, f'Mensaje {estado} exitosamente.')
    return redirect('admin_mensajes')
