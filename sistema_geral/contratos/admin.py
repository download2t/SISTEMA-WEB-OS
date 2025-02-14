from django.contrib import admin
from .models import Contrato

class ContratoAdmin(admin.ModelAdmin):
    # Definindo os campos a serem exibidos na listagem
    list_display = ('documento', 'razao_social', 'nome_fantasia', 'telefone', 'email', 'data_assinatura', 'data_validade', 'valor', 'ativo')
    list_filter = ('ativo', 'data_assinatura', 'data_validade')
    search_fields = ('documento', 'razao_social', 'nome_fantasia', 'email')
    list_editable = ('ativo',)
    fields = ('documento', 'razao_social', 'nome_fantasia', 'telefone', 'email', 'descricao', 'data_assinatura', 'data_validade', 'valor', 'ativo')
    list_display_links = ('documento',)
    ordering = ('-data_assinatura',)  # Ordenando pela data de assinatura, do mais recente para o mais antigo
    list_filter = ('ativo',)


# Registrando o modelo no admin com a configuração personalizada
admin.site.register(Contrato, ContratoAdmin)
