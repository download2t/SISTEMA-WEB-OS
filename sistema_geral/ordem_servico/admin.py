from django.contrib import admin
from .models import Chamado, Mensagem, Evidencia, Contato

# Admin para Chamado
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id','assunto', 'descricao', 'grupo_responsavel', 'prioridade','status', 'criado_por')
    search_fields = ['assunto', 'descricao','id']
    list_filter = ['grupo_responsavel', 'status']
    date_hierarchy = 'data_abertura'

admin.site.register(Chamado, ChamadoAdmin)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome_responsavel', 'numero_telefone', 'grupo','usuario')
    search_fields = ('nome_responsavel', 'numero_telefone', 'grupo__name')


#admin.site.register(Mensagem)
#admin.site.register(Evidencia)
