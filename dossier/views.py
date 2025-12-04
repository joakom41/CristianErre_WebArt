from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import DossierForm
from .models import Dossier, DossierObra
from catalogo.models import Obra

@staff_member_required
def crear_dossier(request):
    """Vista para crear y generar el dossier"""
    if request.method == 'POST':
        form = DossierForm(request.POST)
        if form.is_valid():
            # Crear el dossier
            dossier = form.save()
            
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
    
    return render(request, 'dossier/crear_dossier.html', {
        'form': form,
        'max_obras': 20
    })


@staff_member_required
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