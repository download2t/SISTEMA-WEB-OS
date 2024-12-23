from django.db import models
from django.contrib.auth.models import User, Group

# models.py
class Chamado(models.Model):
    STATUS_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Em andamento', 'Em andamento'),
        ('Encaminhado a TOTVS', 'Encaminhado a TOTVS'),
        ('Concluído', 'Concluído'),
        ('Aguardando aprovação', 'Aguardando aprovação'),
        ('Em análise', 'Em análise'),
        ('Em desenvolvimento', 'Em desenvolvimento'),
        ('Manutenção', 'Manutenção'),
    ]
    
    PRIORIDADE_CHOICES = [  # Prioridade do analista
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
        ('Urgente', 'Urgente'),
    ]
    assunto = models.CharField(max_length=255)
    descricao = models.TextField()
    grupo_responsavel = models.ForeignKey(Group, on_delete=models.CASCADE)
    evidencia = models.FileField(upload_to='evidencias/', null=True, blank=True)  # Evidências associadas diretamente ao chamado
    grupos_liberados = models.ManyToManyField(Group, related_name='chamados_liberados', blank=True)  # Novos grupos liberados
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES)
    prioridade_cliente = models.CharField(max_length=10, null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    numero_ticket = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.assunto

# Modelo para evidências associadas ao chamado
class Evidencia(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='evidencias')  # Relacionamento com Chamado
    arquivo = models.FileField(upload_to='chamados_evidencias/')  # Arquivo da evidência
    descricao = models.CharField(max_length=255, blank=True, null=True)  # Descrição opcional para a evidência

    def __str__(self):
        return self.descricao or self.arquivo.name

# Modelo para mensagens trocadas dentro do chamado
class Mensagem(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='mensagens')  # Relacionamento com Chamado
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()  # Texto da mensagem
    arquivo = models.FileField(upload_to='evidencias/', null=True, blank=True)  # Arquivo anexado à mensagem
    data_envio = models.DateTimeField(auto_now_add=True)  # Data de envio da mensagem

    def __str__(self):
        return f'Mensagem de {self.usuario.username} em {self.data_envio}'

# Modelo para evidências associadas a uma mensagem
class MensagemEvidencia(models.Model):
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE, related_name='evidencias')  # Relacionamento com Mensagem
    arquivo = models.FileField(upload_to='mensagens_evidencias/')  # Arquivo da evidência
    descricao = models.CharField(max_length=255, blank=True, null=True)  # Descrição opcional da evidência

    def __str__(self):
        return self.descricao or self.arquivo.name


class Notificacao(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='notificacoes')
    usuario_destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes_recebidas')
    mensagem = models.CharField(max_length=255)  # Mensagem da notificação
    data_envio = models.DateTimeField(auto_now_add=True)
    visualizada = models.BooleanField(default=False)  # Flag para indicar se a notificação foi visualizada

    def __str__(self):
        return f'Notificação para {self.usuario_destinatario.username} sobre {self.chamado.assunto}'

class Contato(models.Model):
    nome_responsavel = models.CharField(max_length=100)  # Nome do responsável
    numero_telefone = models.CharField(max_length=20)  # Número de telefone
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)  # Grupo responsável (representando o setor)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Vinculação ao usuário

    def __str__(self):
        return f"{self.nome_responsavel} - {self.grupo.name}"

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'