from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class TipoMassagem(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    duracao_minutos = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    ativo = models.BooleanField(default=True, verbose_name='Ativo',
                              help_text='Desmarque para inativar temporariamente esta massagem')

    class Meta:
        verbose_name = 'Tipo de Massagem'
        verbose_name_plural = 'Tipos de Massagem'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.duracao_minutos}min ({'Ativo' if self.ativo else 'Inativo'})"

    def clean(self):
        """Validação para evitar inativar massagem com agendamentos futuros"""
        if not self.ativo and self.agendamento_set.filter(status__in=['agendado', 'confirmado']).exists():
            raise ValidationError('Não é possível inativar uma massagem com agendamentos futuros pendentes')

    def delete(self, *args, **kwargs):
        """Soft delete - marca como inativo em vez de excluir"""
        self.ativo = False
        self.save()

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
        ('em_andamento', 'Em Andamento'),
    ]

    EXPERIENCE_CHOICES = [
        (True, 'Primeira vez'),
        (False, 'Cliente retornando'),
    ]

    # Informações básicas
    nome_hospede = models.CharField(max_length=100, verbose_name='Nome do Hóspede')
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    numero_quarto = models.CharField(max_length=10, blank=True, verbose_name='Número do Quarto')
    numero_reserva = models.CharField(max_length=20, blank=True, verbose_name='Número da Reserva')
    
    # Dados do agendamento
    data = models.DateField()
    horario = models.TimeField(verbose_name='Horário')
    tipo_massagem = models.ForeignKey(TipoMassagem, on_delete=models.PROTECT, verbose_name='Tipo de Massagem')
    
    # Status e controle
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='agendado')
    primeira_vez = models.BooleanField('Primeira vez no spa?', choices=EXPERIENCE_CHOICES, default=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True, verbose_name='Data de Cancelamento')
    motivo_cancelamento = models.TextField(blank=True, verbose_name='Motivo do Cancelamento')
    data_realizacao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Realização')
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data', 'horario']
        permissions = [
            ('cancelar_agendamento', 'Pode cancelar agendamentos'),
            ('confirmar_agendamento', 'Pode confirmar agendamentos'),
            ('registrar_realizacao', 'Pode registrar realização de serviço'),
        ]

    def __str__(self):
        status = self.get_status_display()
        return f"{self.nome_hospede} - {self.data.strftime('%d/%m/%Y')} {self.horario.strftime('%H:%M')} ({status})"
