from django.contrib import admin
from .models import Contrato

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('documento', 'razao_social', 'nome_fantasia', 'telefone', 'email', 'data_assinatura', 'data_validade', 'valor', 'grupo_responsavel', 'ativo')
    list_filter = ('ativo', 'data_assinatura', 'data_validade', 'grupo_responsavel')
    search_fields = ('documento', 'razao_social', 'nome_fantasia', 'email')
    list_editable = ('ativo',)
    fields = ('documento', 'razao_social', 'nome_fantasia', 'telefone', 'email', 'descricao', 'data_assinatura', 'data_validade', 'valor', 'ativo', 'grupo_responsavel')
    list_display_links = ('documento',)
    ordering = ('-data_assinatura',)  # Ordenando pela data de assinatura

admin.site.register(Contrato, ContratoAdmin)
