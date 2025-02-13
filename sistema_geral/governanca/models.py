from django.db import models

class ItemLavanderia(models.Model):
    nome = models.CharField(max_length=100)
    pesokg = models.DecimalField(max_digits=10, decimal_places=2)
    valormedio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class RelatorioLav(models.Model):
    adata = models.DateTimeField()
    vrTotal = models.DecimalField(max_digits=10, decimal_places=2)
    pesoTotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Relatório {self.adata.strftime('%Y-%m-%d')}"

class ItemRelLavanderia(models.Model):
    relatorio = models.ForeignKey(RelatorioLav, on_delete=models.CASCADE)
    item_lavanderia = models.ForeignKey(ItemLavanderia, on_delete=models.CASCADE)
    qtd_itens = models.IntegerField()
    qtd_relavagens = models.IntegerField(default=0) 
    pesokg = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    valormedio = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    relavagemkg = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    class Meta:
        unique_together = ('relatorio', 'item_lavanderia')

    def __str__(self):
        return f"{self.qtd_itens}x {self.item_lavanderia.nome} no relatório {self.relatorio.adata.strftime('%Y-%m-%d')}"
