from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Obra, Artista # Importo mis modelos

def lista_obras(request):
    """
    Mi vista principal que muestra la lista de obras con paginación y filtrado.
    """
    
    # 1. Iniciar con todas las obras que NO estén archivadas
    obras_list = Obra.objects.exclude(estado='ARCHIVADO')
    
    # -----------------------------------------------------------
    # 2. FILTRO 1: Lógica de Filtrado por Estilo (Parámetro 'estilo')
    # Uso request.GET para obtener el parámetro de la URL (ej: ?estilo=Muralismo)
    # -----------------------------------------------------------
    estilo_nombre = request.GET.get('estilo')
    if estilo_nombre:
        # Filtro por el nombre del estilo a través de la relación ManyToMany
        obras_list = obras_list.filter(estilos__nombre=estilo_nombre)
    
    # -----------------------------------------------------------
    # 3. FILTRO 2: Lógica de Filtrado por Estado (Parámetro 'estado')
    # -----------------------------------------------------------
    estado = request.GET.get('estado')
    if estado:
        obras_list = obras_list.filter(estado=estado)
    
    # -----------------------------------------------------------
    # 4. FILTRO 3: Lógica de Filtrado por Artista (Parámetro 'artista')
    # Uso request.GET.get para obtener el ID del Artista (ej: ?artista=1)
    # -----------------------------------------------------------
    artista_id = request.GET.get('artista')
    if artista_id:
        # Filtro por la clave foránea (ID del Artista)
        obras_list = obras_list.filter(artista_id=artista_id)
    
    # 5. Ordenar resultados
    obras_list = obras_list.order_by('-creado')
    
    # 6. Paginación (Necesario para la vista del catálogo)
    paginator = Paginator(obras_list, 6) # Muestro 6 obras por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 7. Contexto
    context = {
        'page_obj': page_obj,
        'artista_seleccionado': artista_id,             
        'estilo_seleccionado': estilo_nombre,
        'estado_seleccionado': estado,
    }
    # No necesitamos incluir artistas ni estilos aquí porque ya vienen del context processor
    
    return render(request, 'catalogo/lista_obras.html', context)