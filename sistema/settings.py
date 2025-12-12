from pathlib import Path
import os  # Asegúrate de importar os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = 'django-insecure-9b&xa$wiclc%wp=zh^cv^!f3#tswme+(&2=bkasw7=x+^-8)&1'
DEBUG = True
ALLOWED_HOSTS = []

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'market',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'sistema.urls'

# Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Para plantillas globales como registration/login.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'market.context_processors.carrito_total',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'sistema.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseña (desactivados para desarrollo)
AUTH_PASSWORD_VALIDATORS = []

# Configuración regional
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos y multimedia
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'market/static'),
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Campo por defecto para claves primarias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones de autenticación
LOGIN_REDIRECT_URL = 'perfil'
LOGOUT_REDIRECT_URL = 'inicio'

# Configuración de sesiones
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Mantiene la sesión después de cerrar el navegador
SESSION_COOKIE_AGE = 1209600  # 2 semanas (en segundos)