from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Contrato(models.Model):
    documento = models.CharField(
        max_length=14,
        verbose_name="CNPJ/CPF",
        help_text="Informe o CNPJ ou CPF (somente números)",
        validators=[RegexValidator(regex=r'^\d+$', message="O campo deve conter apenas números.")],
    )
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome Fantasia", blank=True, null=True)
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        help_text="Informe o telefone com DDD (ex: 45999999999)",
        blank=True, null=True
    )
    email = models.EmailField(blank=True, max_length=50, verbose_name="E-mail")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    data_assinatura = models.DateField(verbose_name="Data de Assinatura")
    data_validade = models.DateField(verbose_name="Data de Validade")
    usuario_responsavel = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário Responsável")
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor do Contrato")
    ativo = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o contrato está ativo ou inativo.")
    email_enviado = models.BooleanField(default=False)

    # NOVO CAMPO PARA O UPLOAD DE ARQUIVO
    arquivo_contrato = models.FileField(
        upload_to='contratos_arquivos/', # Subpasta dentro de MEDIA_ROOT para armazenar os arquivos
        blank=True, 
        null=True, 
        verbose_name="Arquivo do Contrato",
        help_text="Faça o upload do arquivo do contrato (PDF, DOCX, JPG, etc.). Tamanho máximo: 20MB."
    )

    def save(self, *args, **kwargs):
        """ Garante que os campos sejam armazenados em CAIXA ALTA """
        self.razao_social = self.razao_social.upper()
        if self.nome_fantasia:
            self.nome_fantasia = self.nome_fantasia.upper()
        if self.descricao:
            self.descricao = self.descricao.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_fantasia or self.razao_social} ({self.documento})"