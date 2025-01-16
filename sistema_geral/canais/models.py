from django.db import models

class Canal(models.Model):
    numero = models.IntegerField()
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return f"Canal {self.numero} - {self.titulo}"

class ListaCanais(models.Model):
    data_criacao = models.DateField()  # Removido auto_now_add
    canais = models.ManyToManyField(Canal, related_name="listas")

    def __str__(self):
        return f"Lista de {self.data_criacao}"
