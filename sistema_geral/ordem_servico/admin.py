from django.contrib import admin
from .models import Chamado, Mensagem, Evidencia, Contato, GrupoTrabalho

# Admin para Chamado
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'assunto', 'descricao', 'grupo_responsavel', 'grupo_trabalho', 'prioridade', 'status', 'criado_por')
    search_fields = ['assunto', 'descricao', 'id']
    list_filter = ['grupo_responsavel', 'grupo_trabalho', 'status']
    date_hierarchy = 'data_abertura'

admin.site.register(Chamado, ChamadoAdmin)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome_responsavel', 'numero_telefone', 'grupo', 'usuario')
    search_fields = ('nome_responsavel', 'numero_telefone', 'grupo__name')

# Admin para GrupoTrabalho
@admin.register(GrupoTrabalho)
class GrupoTrabalhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_grupo')
    search_fields = ('nome_grupo',)

# Admin para Mensagem
@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'chamado', 'usuario', 'data_envio')
    search_fields = ('chamado__assunto', 'usuario__username')
    list_filter = ('data_envio',)

# Admin para Evidencia
@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'chamado', 'arquivo', 'descricao')
    search_fields = ('chamado__assunto', 'descricao')


#admin.site.register(Mensagem)
#admin.site.register(Evidencia)
