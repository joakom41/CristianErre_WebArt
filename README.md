<div align="center">
  <h1>Cristian Erre - Portfolio & Catálogo de Arte</h1>
  <p>
    Plataforma web minimalista y elegante diseñada para el artista visual y muralista <strong>Cristian Erre</strong>.<br>
    Este proyecto sirve como portafolio digital, catálogo de obras y punto de contacto para clientes y admiradores.
  </p>
</div>

<br>

## 🎨 Características

*   **Diseño "Noir Fluide"**: Estética moderna, minimalista y sofisticada utilizando Tailwind CSS.
*   **Catálogo Interactivo**: Sistema de filtrado avanzado para obras por **Estilo** (Mural, Ilustración, Pintura) y **Estado** (Disponible, Vendido, Solo Cotización).
*   **Gestión de Contenido**: Panel de administración de Django personalizado para subir, editar y gestionar obras de arte fácilmente.
*   **Secciones Informativas**: 
    *   **Home**: Portada impactante con obras destacadas.
    *   **El Artista**: Biografía y trayectoria.
    *   **Historia**: Línea de tiempo interactiva.
    *   **Contacto**: Formulario directo para consultas y cotizaciones.
*   **Página 404 Personalizada**: Manejo de errores elegante con diseño acorde al sitio.
*   **Responsive Design**: Experiencia de usuario fluida y adaptada perfectamente a dispositivos móviles, tablets y escritorio.
*   **Animaciones**: Integración de AOS (Animate On Scroll) para transiciones suaves y elegantes.

## 🛠️ Tecnologías Utilizadas

*   **Backend**: Python 3, Django 5.
*   **Frontend**: HTML5, Tailwind CSS (CDN), JavaScript.
*   **Base de Datos**: SQLite (Configuración por defecto para desarrollo).
*   **Librerías Clave**: 
    *   `django-crispy-forms`: Para formularios elegantes.
    *   `pillow`: Para el procesamiento y manejo de imágenes.

## 🚀 Instalación y Configuración

Sigue estos pasos para levantar el proyecto en tu entorno local:

### 1. Prerrequisitos
*   Python 3.10 o superior instalado.
*   Git instalado.

### 2. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/cristianerre_art.git
cd cristianerre_art
```

### 3. Crear y activar un entorno virtual
Es recomendable usar un entorno virtual para aislar las dependencias.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar la base de datos
Aplica las migraciones para crear la estructura de la base de datos.
```bash
python manage.py migrate
```

### 6. Crear un superusuario (Admin)
Para acceder al panel de administración y gestionar las obras.
```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000/` en tu navegador para ver el sitio.
Accede a `http://127.0.0.1:8000/admin/` para gestionar el contenido.

## 📂 Estructura del Proyecto

*   `core/`: Aplicación principal. Maneja las vistas estáticas (Home, Bio, Contacto), la configuración base de templates y los archivos estáticos globales.
*   `catalogo/`: Aplicación del catálogo. Contiene los modelos de `Obra`, `Artista`, `Estilo` y la lógica de filtrado y visualización.
*   `cristianerre_art/`: Configuración principal del proyecto Django (`settings.py`, `urls.py`, `wsgi.py`).
*   `media/`: Directorio donde se almacenan las imágenes subidas por el usuario (obras de arte).
*   `templates/`: Plantillas HTML base y compartidas.

## ✨ Uso del Panel de Administración

El sitio es completamente dinámico. Desde el panel de admin puedes:
1.  **Crear Estilos**: Define categorías como "Muralismo", "Digital", "Óleo".
2.  **Registrar Obras**: Sube imágenes, asigna títulos, descripciones, precios (opcional) y estados.
3.  **Gestionar Estados**: Cambia una obra de "Disponible" a "Vendido" o "Cotización" instantáneamente.

## 📞 Contacto y Redes

<div align="center">
  <p>
    <strong>Instagram</strong>: <a href="https://www.instagram.com/cristian_erre/">@cristian_erre</a> | 
    <strong>Web</strong>: <a href="https://cristianerre.com">cristianerre.com</a>
  </p>
</div>

<br>

<div align="center">
  <p>© 2025 Cristian Erre. Todos los derechos reservados.</p>
</div>
