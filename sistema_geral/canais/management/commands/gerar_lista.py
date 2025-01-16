from django.core.management.base import BaseCommand
from canais.models import ListaCanais, Canal

class Command(BaseCommand):
    help = 'Gera uma nova lista semanal de canais'

    def handle(self, *args, **kwargs):
        canais = Canal.objects.all()
        lista = ListaCanais.objects.create()
        lista.canais.set(canais)
        lista.save()
        self.stdout.write(self.style.SUCCESS(f'Lista semanal criada em {lista.data_criacao}'))

#python manage.py gerar_lista
