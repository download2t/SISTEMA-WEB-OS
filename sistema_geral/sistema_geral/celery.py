import os
from celery import Celery
from celery.schedules import crontab


# Define configurações padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_geral.settings')


app = Celery('seu_projeto')

# Carrega configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre e registra automaticamente tasks nos apps Django
app.autodiscover_tasks()

# Configuração do Celery Beat

from celery.schedules import crontab

app.conf.beat_schedule = {
    'verificar_contratos_vencendo_task': {
        'task': 'contratos.tasks.verificar_contratos_vencendo', 
        'schedule': crontab(hour=7, minute=55),
    },
}

