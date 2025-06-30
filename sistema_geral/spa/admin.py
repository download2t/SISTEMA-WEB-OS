from django.contrib import admin
from .models import TipoMassagem, Agendamento

@admin.register(TipoMassagem)
class TipoMassagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)
    list_filter = ('duracao_minutos',)
    ordering = ('nome',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_hospede', 'data', 'horario',
        'tipo_massagem', 'numero_quarto', 'numero_reserva'
    )
    search_fields = ('nome_hospede', 'numero_quarto', 'numero_reserva')
    list_filter = ('data', 'tipo_massagem')
    ordering = ('data', 'horario')
    autocomplete_fields = ('tipo_massagem',)
