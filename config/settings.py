"""
config/settings.py — Restaurante Pasta La Vista
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Seguridad ──────────────────────────────────────────────
SECRET_KEY = 'django-insecure-pasta-la-vista-2026-cambiar-en-produccion'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ── Aplicaciones ───────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion',                        # ← nuestra app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Busca templates dentro de cada app automáticamente
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # ← necesario para nav active
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  # ← mensajes
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ── Base de datos — SQL Server ──────────────────────────────
# Requiere: pip install mssql-django
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'restaurante_501',          # nombre de tu BD en SSMS
        'HOST': 'EDWAR\\SQLEXPRESS',        # tu servidor (ver imagen SSMS)
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',    # usa autenticación de Windows
        },
    }
}

# ── Validación de contraseñas ───────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internacionalización ────────────────────────────────────
LANGUAGE_CODE = 'es-co'
TIME_ZONE     = 'America/Bogota'
USE_I18N      = True
USE_TZ        = True

# ── Archivos estáticos ─────────────────────────────────────
STATIC_URL = '/static/'
# Django buscará estáticos dentro de cada app (APP_DIRS=True ya lo hace)
# Si quieres una carpeta global adicional, descomenta:
# STATICFILES_DIRS = [BASE_DIR / 'static']

# ── Login / Logout ─────────────────────────────────────────
LOGIN_URL          = '/login/'          # redirige aquí si no está autenticado
LOGIN_REDIRECT_URL = '/'                # después de login exitoso
LOGOUT_REDIRECT_URL = '/login/'         # después de logout

# ── Clave primaria por defecto ──────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Mensajes — etiquetas compatibles con nuestro CSS ───────
from django.contrib.messages import constants as messages_constants
MESSAGE_TAGS = {
    messages_constants.DEBUG:   'info',
    messages_constants.INFO:    'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR:   'error',
}
