from django.db import models
from django.contrib.auth.models import User, Group

# Modelo para grupo de trabalho
class GrupoTrabalho(models.Model):
    nome_grupo = models.CharField(max_length=255)  # Ajustei o tamanho do max_length para um valor mais razoável.

    def __str__(self):
        return self.nome_grupo

# Modelo para chamados de suporte
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
    
    PRIORIDADE_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
        ('Urgente', 'Urgente'),
    ]
    
    assunto = models.CharField(max_length=255)
    descricao = models.TextField()
    grupo_responsavel = models.ForeignKey(Group, on_delete=models.CASCADE)
    grupo_trabalho = models.ForeignKey(GrupoTrabalho, null=True, on_delete=models.CASCADE) 
    evidencia = models.FileField(upload_to='evidencias/', null=True, blank=True)
    grupos_liberados = models.ManyToManyField(Group, related_name='chamados_liberados', blank=True)
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
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='evidencias')
    arquivo = models.FileField(upload_to='chamados_evidencias/')
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.descricao or self.arquivo.name

# Modelo para mensagens dentro do chamado
class Mensagem(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='mensagens')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    arquivo = models.FileField(upload_to='evidencias/', null=True, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensagem de {self.usuario.username} em {self.data_envio}'

# Modelo para evidências associadas a uma mensagem
class MensagemEvidencia(models.Model):
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE, related_name='evidencias')
    arquivo = models.FileField(upload_to='mensagens_evidencias/')
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.descricao or self.arquivo.name

# Modelo para notificações associadas a chamados
class Notificacao(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='notificacoes')
    usuario_destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes_recebidas')
    mensagem = models.CharField(max_length=255)
    data_envio = models.DateTimeField(auto_now_add=True)
    visualizada = models.BooleanField(default=False)

    def __str__(self):
        return f'Notificação para {self.usuario_destinatario.username} sobre {self.chamado.assunto}'

# Modelo para contatos dentro do sistema
class Contato(models.Model):
    nome_responsavel = models.CharField(max_length=100)
    numero_telefone = models.CharField(max_length=20)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome_responsavel} - {self.grupo.name}"

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
