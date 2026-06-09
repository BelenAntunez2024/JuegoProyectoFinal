
import os
from pathlib import Path
import environ # Importamos la librería


# Inicializamos el entorno
env = environ.Env(
    # Establecemos valores por defecto si fuera necesario
    DEBUG=(bool, False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Leemos el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'juego',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# ==============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS (POSTGRESQL)
# ==============================================================================
# Leemos las credenciales sensibles desde el archivo .env usando 'django-environ'.
# Esto evita subir contraseñas o datos críticos al repositorio de Git.
DATABASES = {
    'default': {
        # Usamos el motor de base de datos oficial de Django para PostgreSQL
        'ENGINE': 'django.db.backends.postgresql',
        # Nombre de la base de datos (leído del .env)
        'NAME': env('DB_NAME'),
        # Usuario de acceso (leído del .env)
        'USER': env('DB_USER'),
        # Contraseña del usuario (leída del .env)
        'PASSWORD': env('DB_PASSWORD'),
        # Dirección IP o nombre de host del contenedor de Postgres en Docker (leído del .env)
        'HOST': env('DB_HOST'),
        # Puerto por defecto de Postgres (5432)
        'PORT': env('DB_PORT', default='5432')
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# ==============================================================================
# CONFIGURACIÓN DE ARCHIVOS DE MEDIA (IMÁGENES SUBIDAS POR EL ADMIN)
# ==============================================================================
# MEDIA_URL: La URL pública desde donde el navegador accede a las imágenes subidas.
# Ej: http://localhost:8000/media/famosos/messi.jpg
MEDIA_URL = '/media/'

# MEDIA_ROOT: La ruta física en el servidor (dentro del contenedor Docker) donde
# Django guarda los archivos subidos. Corresponde a la carpeta /app/media/
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
