from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True,
        related_name="categorias"
    )  # Nulo para categorias coletivas
    is_coletiva = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Senha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senhas")  # Quem criou a senha
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="senhas")
    descricao = models.CharField(max_length=255)  # Descrição da senha
    user = models.CharField(max_length=255, blank=True, null=True)  # O login
    senha = models.CharField(max_length=255)  # A senha
    link = models.URLField(blank=True, null=True)  # Link de acesso
    is_coletiva = models.BooleanField(default=False)  # Define se a senha é coletiva

    def __str__(self):
        return f"{self.descricao} - {'Coletiva' if self.is_coletiva else 'Pessoal'}"

    def pode_ser_visualizada_por(self, usuario):
        """Verifica se a senha pode ser visualizada por um usuário."""
        return self.is_coletiva or self.usuario == usuario