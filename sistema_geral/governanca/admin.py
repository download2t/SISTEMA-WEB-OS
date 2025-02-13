from django.contrib import admin
from django.db import transaction
from governanca.models import ItemLavanderia, RelatorioLav, ItemRelLavanderia

# Registro do modelo ItemLavanderia
@admin.register(ItemLavanderia)
class ItemLavanderiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pesokg', 'valormedio')
    search_fields = ('nome',)
    list_filter = ('nome',)

# Registro do modelo RelatorioLav
@admin.register(RelatorioLav)
class RelatorioLavAdmin(admin.ModelAdmin):
    list_display = ('adata', 'vrTotal', 'pesoTotal')
    search_fields = ('adata',)
    list_filter = ('adata',)

    def save_model(self, request, obj, form, change):
        # Garantir que a criação do relatório também registre os itens de lavanderia automaticamente
        with transaction.atomic():
            obj.save()
            # Registrar os itens de lavanderia relacionados ao relatório
            for item in ItemLavanderia.objects.all():
                ItemRelLavanderia.objects.create(
                    relatorio=obj,
                    item_lavanderia=item,
                    qtd_itens=0,  # Este valor pode ser alterado conforme necessário
                    qtd_relavagens=0,  # Este valor pode ser alterado conforme necessário
                    pesokg=0,  # Este valor pode ser alterado conforme necessário
                    valormedio=item.valormedio,
                    relavagemkg=0  # Este valor pode ser alterado conforme necessário
                )

# Registro do modelo ItemRelLavanderia
@admin.register(ItemRelLavanderia)
class ItemRelLavanderiaAdmin(admin.ModelAdmin):
    list_display = ('relatorio', 'item_lavanderia', 'qtd_itens', 'qtd_relavagens', 'pesokg', 'valormedio', 'relavagemkg')
    search_fields = ('relatorio__adata', 'item_lavanderia__nome')
    list_filter = ('relatorio__adata', 'item_lavanderia__nome')
    raw_id_fields = ('relatorio', 'item_lavanderia')
