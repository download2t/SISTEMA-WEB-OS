from django.db import models

# Modelo para armazenar instruções do rodapé do PDF
class InstrucoesPDF(models.Model):
    texto = models.TextField("Instruções para rodapé do PDF", blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Instruções do PDF"
from django.contrib.auth.models import Group
from django.db import models


class Ramal(models.Model):
    numero_ramal = models.CharField(max_length=10, unique=True)
    linha_completa = models.CharField(max_length=20)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='ramais')
    atendente = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)  # Novo campo 'ativo', padrão é True (ativo)
    instrucoes_pdf = models.TextField(
        blank=True,
        verbose_name="Instruções para rodapé do PDF",
        help_text="Instruções como: como fazer ligação, puxar ligação, etc."
    )

    def __str__(self):
        return f"{self.numero_ramal} - {self.atendente}"
