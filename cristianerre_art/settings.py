"""
Django settings for cristianerre_art project.
"""

from pathlib import Path
from django.conf import settings 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-lxi3_5#e5oqihsy45=rrnfu_=*l2yaz4jp&%-svt+z(8971=vg'

# Para probar la página 404 personalizada debemos ejecutar con DEBUG = False.

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] # Añado hosts por buena práctica

# ----------------------------------------------------
# APLICACIONES INSTALADAS (INSTALLED_APPS)
# ----------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',

    'core',
    'catalogo',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cristianerre_art.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS para templates compartidos a nivel de proyecto (Incluye el 404.html)
        'DIRS': [
            BASE_DIR / 'cristianerre_art' / 'templates',
            BASE_DIR / 'templates'
        ], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Dejo este por si acaso
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Mis Procesadores de Contexto personalizados (R5)
                'core.context_processors.banner_imagen',
                # Añado los procesadores que usaré para los filtros del menú (R5)
                'core.context_processors.estilos_disponibles', 
                'core.context_processors.artistas_disponibles',
            ],
        },
    },
]

WSGI_APPLICATION = 'cristianerre_art.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# ----------------------------------------------------
# INTERNACIONALIZACIÓN (R: Lenguaje y Hora)
# ----------------------------------------------------
LANGUAGE_CODE = 'es' 
TIME_ZONE = 'America/Santiago' 
USE_I18N = True 
USE_TZ = True

# ARCHIVOS ESTÁTICOS (STATIC FILES)
# ----------------------------------------------------
STATIC_URL = '/static/'
# Directorio donde `collectstatic` copiará todos los archivos en producción
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]

# ----------------------------------------------------
# ARCHIVOS MEDIA (Imágenes subidas)
# ----------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------
# CONFIGURACIÓN DE CRISPY FORMS (R6)
# ----------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


