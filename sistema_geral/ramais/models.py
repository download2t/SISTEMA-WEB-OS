from django.contrib.auth.models import Group
from django.db import models

class Ramal(models.Model):
    numero_ramal = models.CharField(max_length=10, unique=True)
    linha_completa = models.CharField(max_length=20)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='ramais')
    atendente = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)  # Novo campo 'ativo', padrão é True (ativo)

    def __str__(self):
        return f"{self.numero_ramal} - {self.atendente}"
