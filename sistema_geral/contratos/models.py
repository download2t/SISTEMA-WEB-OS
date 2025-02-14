from django.db import models
from django.core.validators import RegexValidator

class Contrato(models.Model):  
    documento = models.CharField(
        max_length=14,  
        unique=True,  
        verbose_name="CNPJ/CPF",
        help_text="Informe o CNPJ ou CPF (somente números)"
    )
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome Fantasia", blank=True, null=True)

    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        validators=[RegexValidator(regex=r'^\+?\d{8,15}$', message="Formato inválido de telefone")],
        help_text="Informe o telefone com DDD (ex: 45999999999)"
    )

    email = models.EmailField(max_length=50, verbose_name="E-mail", unique=True)

    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)

    data_assinatura = models.DateField(verbose_name="Data de Assinatura")
    data_validade = models.DateField(verbose_name="Data de Validade")

    valor = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Valor do Contrato"
    )
    
    ativo = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o contrato está ativo ou inativo.")
    email_enviado = models.BooleanField(default=False)


    def __str__(self):  
        return f"{self.nome_fantasia or self.razao_social} ({self.documento})"
