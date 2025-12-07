from django.shortcuts import render, redirect, get_object_or_404
"""Vistas de dossier accesibles para todos los usuarios."""
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import DossierForm
from .models import Dossier, DossierObra
from catalogo.models import Obra

def crear_dossier(request):
    """Vista para crear y generar el dossier"""
    es_staff = request.user.is_authenticated and request.user.is_staff

    # Datos bloqueados del artista para usuarios no staff/no registrados
    artista_nombre = 'Cristian Erre'
    artista_bio = (
        'Cristian Erre es un artista visual con una década de trayectoria, reconocido por su versatilidad al moverse '
        'entre el óleo clásico y la ilustración digital contemporánea. Su trabajo explora temas de identidad urbana '
        'y fragmentación del paisaje. Graduado de la Academia de Bellas Artes, Cristian ha expuesto en galerías de '
        'Santiago y Valparaíso. En los últimos años, su enfoque en el muralismo ha ganado notoriedad, buscando llevar '
        'el arte a gran escala a espacios públicos y privados.'
    )
    artista_foto = 'https://i.imgur.com/unFLwMZ.png'

    if request.method == 'POST':
        post_data = request.POST.copy()
        if not es_staff:
            post_data['nombre_artista'] = artista_nombre
            post_data['bio_artista'] = artista_bio
            post_data['foto_artista_url'] = artista_foto
        form = DossierForm(post_data)
        if form.is_valid():
            dossier = form.save(commit=False)
            # Forzar datos del artista para usuarios no staff/no registrados
            if not es_staff:
                dossier.nombre_artista = artista_nombre
                dossier.bio_artista = artista_bio
                dossier.foto_artista_url = artista_foto

            dossier.save()
            
            # Procesar obras seleccionadas
            obras_ids = []
            for i in range(1, 21):  # Máximo 20 obras
                field_name = f'obra_{i}'
                if field_name in request.POST and request.POST[field_name]:
                    obra_id = request.POST[field_name]
                    if obra_id:
                        obras_ids.append((int(obra_id), i))
            
            # Guardar relaciones con orden
            for obra_id, orden in obras_ids:
                try:
                    obra = Obra.objects.get(id=obra_id)
                    DossierObra.objects.create(
                        dossier=dossier,
                        obra=obra,
                        orden=orden
                    )
                except Obra.DoesNotExist:
                    pass
            
            # Generar PDF
            return generar_pdf(request, dossier.id)
    else:
        form = DossierForm()
        if not es_staff:
            # Precargar y bloquear campos del artista para vista
            form.fields['nombre_artista'].initial = artista_nombre
            form.fields['bio_artista'].initial = artista_bio
            form.fields['foto_artista_url'].initial = artista_foto
            form.fields['nombre_artista'].widget.attrs['readonly'] = True
            form.fields['bio_artista'].widget.attrs['readonly'] = True
            form.fields['foto_artista_url'].widget.attrs['readonly'] = True
            form.fields['nombre_artista'].widget.attrs['class'] = form.fields['nombre_artista'].widget.attrs.get('class', '') + ' bg-stone-100'
            form.fields['bio_artista'].widget.attrs['class'] = form.fields['bio_artista'].widget.attrs.get('class', '') + ' bg-stone-100'
            form.fields['foto_artista_url'].widget.attrs['class'] = form.fields['foto_artista_url'].widget.attrs.get('class', '') + ' bg-stone-100'
    
    return render(request, 'dossier/crear_dossier.html', {
        'form': form,
        'max_obras': 20,
        'es_staff': es_staff
    })


def generar_pdf(request, dossier_id):
    """Genera el PDF del dossier o descarga HTML si WeasyPrint no está disponible"""
    dossier = get_object_or_404(Dossier, id=dossier_id)
    obras_ordenadas = dossier.dossierobra_set.all().select_related('obra').prefetch_related('obra__estilos', 'obra__artista')
    
    # Renderizar HTML
    html_string = render_to_string('dossier/pdf_template.html', {
        'dossier': dossier,
        'obras': obras_ordenadas
    })
    
    # Intentar generar PDF con WeasyPrint
    try:
        from weasyprint import HTML
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()
        
        # Responder con el PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="dossier_{dossier.nombre_artista}.pdf"'
        return response
        
    except (ImportError, OSError) as e:
        # Si WeasyPrint no está disponible, ofrecer descarga HTML
        response = HttpResponse(html_string, content_type='text/html')
        response['Content-Disposition'] = f'inline; filename="dossier_{dossier.nombre_artista}.html"'
        
        # Agregar aviso en la página
        aviso = f'''
        <div style="position: fixed; top: 0; left: 0; right: 0; background: #fef3c7; border-bottom: 2px solid #f59e0b; padding: 15px; text-align: center; z-index: 9999;">
            <p style="margin: 0; color: #92400e; font-weight: bold;">⚠️ Modo de Vista HTML</p>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #78350f;">
                WeasyPrint no está configurado. Puedes imprimir esta página como PDF desde tu navegador (Ctrl+P → Guardar como PDF)
                o <a href="https://github.com/Kozea/WeasyPrint/releases" target="_blank" style="color: #c2410c; text-decoration: underline;">instalar WeasyPrint con GTK</a>.
            </p>
        </div>
        <div style="height: 100px;"></div>
        '''
        html_with_notice = html_string.replace('<body>', '<body>' + aviso)
        
        response = HttpResponse(html_with_notice, content_type='text/html')
        return response

# --- VISTA SOLO LECTURA PARA USUARIOS NO STAFF ---
def dossier_artista_readonly(request):
    if request.user.is_staff:
        return redirect('crear_dossier')  # Redirige a la vista normal si es staff
    contexto = {
        'nombre': 'Cristian Erre',
        'foto_url': 'https://i.imgur.com/unFLwMZ.png',
        'bio_parrafos': [
            'Cristian Erre es un artista visual con una década de trayectoria, reconocido por su versatilidad al moverse entre el óleo clásico y la ilustración digital contemporánea. Su trabajo explora temas de identidad urbana y fragmentación del paisaje.',
            'Graduado de la Academia de Bellas Artes, Cristian ha expuesto en galerías de Santiago y Valparaíso. En los últimos años, su enfoque en el muralismo ha ganado notoriedad, buscando llevar el arte a gran escala a espacios públicos y privados.'
        ]
    }
    return render(request, 'dossier/dossier_artista_readonly.html', contexto)

def dossier_artista_pdf(request):
    if request.user.is_staff:
        return redirect('crear_dossier')
    contexto = {
        'nombre': 'Cristian Erre',
        'foto_url': 'https://i.imgur.com/unFLwMZ.png',
        'bio_parrafos': [
            'Cristian Erre es un artista visual con una década de trayectoria, reconocido por su versatilidad al moverse entre el óleo clásico y la ilustración digital contemporánea. Su trabajo explora temas de identidad urbana y fragmentación del paisaje.',
            'Graduado de la Academia de Bellas Artes, Cristian ha expuesto en galerías de Santiago y Valparaíso. En los últimos años, su enfoque en el muralismo ha ganado notoriedad, buscando llevar el arte a gran escala a espacios públicos y privados.'
        ]
    }
    return render(request, 'dossier/dossier_artista_pdf.html', contexto)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def generar_pdf_bloqueado(request):
    if request.method == 'POST' and not request.user.is_staff:
        from django.template.loader import render_to_string
        html_string = render_to_string('dossier/dossier_artista_pdf.html', {
            'nombre': 'Cristian Erre',
            'foto_url': 'https://i.imgur.com/unFLwMZ.png',
            'bio_parrafos': [
                'Cristian Erre es un artista visual con una década de trayectoria, reconocido por su versatilidad al moverse entre el óleo clásico y la ilustración digital contemporánea. Su trabajo explora temas de identidad urbana y fragmentación del paisaje.',
                'Graduado de la Academia de Bellas Artes, Cristian ha expuesto en galerías de Santiago y Valparaíso. En los últimos años, su enfoque en el muralismo ha ganado notoriedad, buscando llevar el arte a gran escala a espacios públicos y privados.'
            ]
        })
        try:
            from weasyprint import HTML
            html = HTML(string=html_string)
            pdf_file = html.write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="dossier_Cristian_Erre.pdf"'
            return response
        except (ImportError, OSError):
            response = HttpResponse(html_string, content_type='text/html')
            response['Content-Disposition'] = 'inline; filename="dossier_Cristian_Erre.html"'
            return response
    return redirect('dossier:dossier_artista_pdf')