import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'mude-isso-em-producao'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', '<SEU_PUBLIC_IP>']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'geoapp',
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

ROOT_URLCONF = 'assignment10.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django automaticamente procura por templates dentro de cada app/ templates/
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

WSGI_APPLICATION = 'assignment10.wsgi.application'

DATABASES = {
    # Você pode usar o SQLite padrão só para o Django (auth, sessions etc.)
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# ---- SUAS CONFIGS DE API E MONGODB ----

# OpenWeatherMap API Key (você pode exportar no shell ou colocar no .env)
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', 'COLOQUE_SUA_KEY_AQUI')

# MongoDB rodando na outra EC2 (use o IP PRIVADO dela)
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://<MONGO_PRIVATE_IP>:27017/')
MONGODB_DB_NAME = 'geo_weather_db'
MONGODB_COLLECTION_NAME = 'search_history'
