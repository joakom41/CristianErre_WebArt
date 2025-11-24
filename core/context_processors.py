from core.models import Banner
from catalogo.models import Estilo, Artista

# -----------------------------------------------------------------
# Context processor 1: Banner para todas las páginas
# -----------------------------------------------------------------
def banner_imagen(request):
    """Mi procesador de contexto para inyectar banners globales en el sitio."""
    try:
        banners = Banner.objects.all()
        return {'banners': banners} 
    except Exception:
        # Uso una lista vacía en caso de que la tabla aún no exista
        return {'banners': []}

# -----------------------------------------------------------------
# Context processor 2: Estilos para Menú de Filtros (¡Resuelve el ImportError!)
# -----------------------------------------------------------------
def estilos_disponibles(request):
    """Mi procesador para inyectar todos los estilos disponibles en el menú de navegación."""
    try:
        # Consulto todos los objetos Estilo ordenados por nombre
        estilos = Estilo.objects.all().order_by('nombre') 
    except Exception:
        # Uso una lista vacía en caso de error
        estilos = Estilo.objects.none()
        
    # Retorno la variable 'estilos_menu' que estará disponible globalmente
    return {'estilos_menu': estilos}

# -----------------------------------------------------------------
# Context processor 3: Artistas para Menú de Filtros
# -----------------------------------------------------------------
def artistas_disponibles(request):
    """Mi procesador para inyectar todos los artistas disponibles en el menú de navegación."""
    try:
        # Consulto todos los objetos Artista ordenados por nombre
        artistas = Artista.objects.all().order_by('nombre')
    except Exception:
        # Uso una lista vacía en caso de error
        artistas = Artista.objects.none()
        
    return {'artistas_menu': artistas}