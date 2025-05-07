from pathlib import Path
from django.contrib.messages import constants as messages
import os
BASE_DIR = Path(__file__).resolve().parent.parent # Build paths inside the project like this: BASE_DIR / 'subdir'.

key_file_path = os.path.join(os.path.dirname(__file__), 'key.txt')

# Ler o valor da chave secreta do arquivo
with open(key_file_path, 'r') as file:
    SECRET_KEY = file.read().strip()

DEBUG = True # SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*', '127.0.0.1', '172.16.10.26','172.16.10.169', 'ti_sanma']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cron',  
    'core',
    'ordem_servico',
    'ramais',
    'banco_senhas',
    'canais',
    'governanca',
    'contratos',
]


MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistema_geral.urls'
import os

# Defina o caminho para a pasta templates no projeto
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  #TEMPLATES *******
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

WSGI_APPLICATION = 'sistema_geral.wsgi.application'

"""
DATABASES = {
        'default': {
        'ENGINE': 'mssql',  # Para SQL Server
        'NAME': 'db_os',
        'USER': 'sa',
        'PASSWORD': 'SanmaMacaco,#21',
        'HOST': '172.16.10.169',
        'PORT': '1433',
        'OPTIONS': {
        'driver': 'ODBC Driver 17 for SQL Server',  
        },
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Define SQLite como o banco de dados
        'NAME': BASE_DIR / 'db_sistema.sqlite3', # Nome do arquivo do banco de dados SQLite
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Altere para o comprimento mínimo desejado
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

# Se você tiver uma pasta de arquivos estáticos no projeto:
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'nao_autenticado'  # Redireciona para a página personalizada se o usuário não estiver logado

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Servidor SMTP do Gmail
EMAIL_PORT = 587  # Porta para TLS
EMAIL_USE_TLS = True  # Habilita o TLS
EMAIL_HOST_USER = 'suportesanma@gmail.com'  # Seu e-mail
EMAIL_HOST_PASSWORD = 'ofdf qopt wduz ahxl'  # Sua senha app ordem_servico
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Define o e-mail padrão para envios


MEDIA_URL = '/media/' # Caminho onde os arquivos de mídia (evidências) serão armazenados

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Caminho absoluto no servidor para salvar os arquivos

FILE_UPLOAD_MAX_MEMORY_SIZE = 20485760  # Limite de 20 MB em upload de chamados

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usar o banco de dados para armazenar sessões
SESSION_COOKIE_AGE = 28800 # Tempo em segundos que a sessão dura (exemplo: 8 horas)

CRONJOBS = [
    ('10 08 * * *', 'myapp.tasks.verificar_contratos_vencendo'), 

    # MINUTO / HORA / 8H e 10 min
]

CSRF_TRUSTED_ORIGINS = [
    #'https://f355-177-87-108-241.ngrok-free.app',
    'https://outgoing-friendly-snake.ngrok-free.app',
]
