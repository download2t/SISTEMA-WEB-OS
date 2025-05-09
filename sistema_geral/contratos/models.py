from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group

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
    blank=True, null=True  # Agora não é obrigatório
    )
    email = models.EmailField(blank=True, max_length=50, verbose_name="E-mail")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    data_assinatura = models.DateField(verbose_name="Data de Assinatura")
    data_validade = models.DateField(verbose_name="Data de Validade")
    grupo_responsavel = models.ForeignKey(Group, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor do Contrato")
    ativo = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o contrato está ativo ou inativo.")
    email_enviado = models.BooleanField(default=False)

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
