from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_fantasia',
        'razao_social',
        'documento', # This is your 'CPF/CNPJ' field
        'telefone',
        'email',
        'data_validade',
        'ativo',
        'email_enviado',
    )
    list_filter = (
        'ativo',
        'email_enviado',
        'data_assinatura',
        'data_validade',
        'usuario_responsavel',
    )
    search_fields = (
        'id',
        'nome_fantasia',
        'razao_social',
        'documento',
        'email',
        'descricao',
    )
    date_hierarchy = 'data_assinatura'
    readonly_fields = ('email_enviado',)
    fieldsets = (
        (None, {
            'fields': (
                'documento',
                'razao_social',
                'nome_fantasia',
                'telefone',
                'email',
                'descricao',
            )
        }),
        ('Datas e Valores', {
            'fields': (
                'data_assinatura',
                'data_validade',
                'valor',
            )
        }),
        ('Responsabilidade e Status', {
            'fields': (
                'usuario_responsavel',
                'ativo',
                'email_enviado',
            )
        }),
        ('Anexo do Contrato', {
            'fields': ('arquivo_contrato',)
        }),
    )

    actions = ['make_inactive', 'mark_emails_sent', 'mark_emails_unsent']

    def make_inactive(self, request, queryset):
        queryset.update(ativo=False)
    make_inactive.short_description = "Marcar contratos selecionados como inativos"

    def mark_emails_sent(self, request, queryset):
        queryset.update(email_enviado=True)
    mark_emails_sent.short_description = "Marcar e-mails selecionados como ENVIADOS"

    def mark_emails_unsent(self, request, queryset):
        queryset.update(email_enviado=False)
    mark_emails_unsent.short_description = "Marcar e-mails selecionados como NÃO ENVIADOS"