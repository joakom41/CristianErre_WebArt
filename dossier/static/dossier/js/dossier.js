document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('obras-container');
    const form = document.getElementById('dossier-form');
    const maxObras = 20;
    let contadorObras = 10;
    
    // Función para crear un nuevo campo de obra
    function crearCampoObra(numero) {
        const div = document.createElement('div');
        div.className = 'obra-row flex items-center gap-3 p-3 bg-stone-50 rounded-lg border border-stone-200';
        
        // Clonar el primer selector para obtener las mismas opciones
        const primerSelect = container.querySelector('select');
        if (!primerSelect) return null;
        
        const nuevoSelect = primerSelect.cloneNode(true);
        nuevoSelect.name = 'obra_' + numero;
        nuevoSelect.id = 'id_obra_' + numero;
        nuevoSelect.value = '';
        nuevoSelect.className = 'flex-1';
        
        // Crear label
        const label = document.createElement('label');
        label.textContent = 'Obra #' + numero;
        label.className = 'text-sm font-medium text-stone-700 min-w-[80px]';
        label.setAttribute('for', nuevoSelect.id);
        
        // Botón eliminar
        const btnEliminar = document.createElement('button');
        btnEliminar.type = 'button';
        btnEliminar.className = 'px-3 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700 transition-colors text-sm font-medium';
        btnEliminar.innerHTML = 'Eliminar';
        btnEliminar.addEventListener('click', function() {
            div.remove();
            contadorObras--;
            actualizarEstadoBotones();
        });
        
        div.appendChild(label);
        div.appendChild(nuevoSelect);
        div.appendChild(btnEliminar);
        
        return div;
    }
    
    // Función para agregar botones de eliminar a obras existentes
    function agregarBotonesEliminar() {
        const obrasExistentes = container.querySelectorAll('.obra-row');
        
        obrasExistentes.forEach(function(row, index) {
            // Verificar si ya tiene un botón de eliminar
            if (row.querySelector('.btn-eliminar-obra')) return;
            
            // Agregar clases para el diseño
            row.className = 'obra-row flex items-center gap-3 p-3 bg-stone-50 rounded-lg border border-stone-200';
            
            // Encontrar el label y añadirle estilos
            const label = row.querySelector('label');
            if (label) {
                label.className = 'text-sm font-medium text-stone-700 min-w-[80px]';
            }
            
            // Encontrar el select y añadirle clase flex-1
            const select = row.querySelector('select');
            if (select) {
                select.className = 'flex-1';
            }
            
            // Crear botón eliminar
            const btnEliminar = document.createElement('button');
            btnEliminar.type = 'button';
            btnEliminar.className = 'btn-eliminar-obra px-3 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700 transition-colors text-sm font-medium';
            btnEliminar.innerHTML = 'Eliminar';
            btnEliminar.addEventListener('click', function() {
                row.remove();
                contadorObras--;
                actualizarEstadoBotones();
            });
            
            row.appendChild(btnEliminar);
        });
    }
    
    // Función para actualizar el estado de los botones
    function actualizarEstadoBotones() {
   
        console.log('Obras actuales:', contadorObras);
    }
    
    // Crear un botón para agregar más obras
    function crearBotonAgregar() {
        const btnContainer = document.createElement('div');
        btnContainer.className = 'mt-6 pt-6 border-t border-stone-200 flex items-center justify-between';
        
        const btnAgregar = document.createElement('button');
        btnAgregar.type = 'button';
        btnAgregar.id = 'agregar-obra-btn';
        btnAgregar.className = 'px-6 py-3 bg-stone-900 text-white rounded-lg hover:bg-stone-800 transition-colors font-medium';
        btnAgregar.innerHTML = 'Agregar Obra';
        
        const info = document.createElement('p');
        info.className = 'text-sm text-stone-600';
        info.innerHTML = 'Obras seleccionadas: <strong id="contador-obras">' + contadorObras + '</strong> / ' + maxObras;
        
        btnAgregar.addEventListener('click', function() {
            if (contadorObras >= maxObras) {
                alert('Has alcanzado el límite máximo de ' + maxObras + ' obras');
                return;
            }
            
            contadorObras++;
            const nuevoCampo = crearCampoObra(contadorObras);
            
            if (nuevoCampo) {
                // Insertar antes del contenedor de botones
                container.appendChild(nuevoCampo);
                
                // Actualizar contador
                const contadorSpan = document.getElementById('contador-obras');
                if (contadorSpan) {
                    contadorSpan.textContent = contadorObras;
                }
                
                // Deshabilitar botón si llegamos al máximo
                if (contadorObras >= maxObras) {
                    btnAgregar.disabled = true;
                    btnAgregar.className = 'px-6 py-3 bg-stone-400 text-white rounded-lg cursor-not-allowed font-medium';
                    btnAgregar.innerHTML = 'Máximo alcanzado';
                }
            }
        });
        
        btnContainer.appendChild(btnAgregar);
        btnContainer.appendChild(info);
        
        // Insertar después del container de obras
        container.parentNode.insertBefore(btnContainer, container.nextSibling);
    }
    
    // Inicializar
    agregarBotonesEliminar();
    crearBotonAgregar();
    
    // Validación antes de enviar el formulario
    if (form) {
        form.addEventListener('submit', function(e) {
            // Contar cuántas obras están realmente seleccionadas
            const selectores = form.querySelectorAll('select[name^="obra_"]');
            let obrasSeleccionadas = 0;
            
            selectores.forEach(function(select) {
                if (select.value && select.value !== '') {
                    obrasSeleccionadas++;
                }
            });
            
            if (obrasSeleccionadas === 0) {
                e.preventDefault();
                alert('Debes seleccionar al menos una obra para generar el dossier');
                return false;
            }
        });
    }
});
