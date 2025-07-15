from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import Contrato # Assumindo que Contrato está no mesmo app
from django.contrib.auth.models import User # Importar o modelo User

@shared_task
def verificar_contratos_vencendo():
    """ 
    Verifica contratos que vencem em menos de 60 dias e envia lembretes automaticamente.
    Os e-mails são enviados para TI, Financeiro e o e-mail do usuário responsável pelo contrato.
    """
    hoje = timezone.now().date() # Usar .date() para comparação com DateField
    data_limite = hoje + timezone.timedelta(days=60)

    # Filtrar contratos que vencem em até 60 dias E que o e-mail ainda não foi enviado
    # A data de validade deve ser maior ou igual a hoje e menor ou igual à data limite
    contratos_a_vencer = Contrato.objects.filter(
        data_validade__gte=hoje,
        data_validade__lte=data_limite,
        email_enviado=False,
        ativo=True # Adicionado para garantir que apenas contratos ativos gerem lembretes
    )

    if not contratos_a_vencer.exists():
        print("Nenhum contrato para enviar lembrete.")
        return

    print(f"Encontrados {contratos_a_vencer.count()} contratos próximos do vencimento.")

    contratos_com_email_enviado = [] # Lista para armazenar IDs de contratos que tiveram email enviado com sucesso

    for contrato in contratos_a_vencer:
        destinatarios = []

        # Adicionar e-mails fixos
        destinatarios.append("ti@sanmahotel.com.br")
        destinatarios.append("financeiro@sanmahotel.com.br")

        # Adicionar o e-mail do usuário responsável, se existir
        if contrato.usuario_responsavel and contrato.usuario_responsavel.email:
            destinatarios.append(contrato.usuario_responsavel.email)
        
        # Remover duplicatas e valores vazios/None
        destinatarios_finais = list(set([email for email in destinatarios if email]))

        if not destinatarios_finais:
            print(f"Nenhum destinatário válido encontrado para o contrato {contrato.id} - {contrato.nome_fantasia}. Pulando envio.")
            continue # Pula para o próximo contrato se não houver destinatários

        try:
            # Gerar conteúdo do e-mail usando template HTML
            context = {
                "contrato": contrato,
                "dias_restantes": (contrato.data_validade - hoje).days, # Calcula dias restantes
            }
            html_content = render_to_string("contratos/lembrete_vencimento.html", context)

            # Configurar e-mail
            assunto = f"Lembrete de Vencimento de Contrato: {contrato.nome_fantasia} - Vence em {context['dias_restantes']} dias"
            
            email = EmailMultiAlternatives(
                subject=assunto,
                body=f"O contrato '{contrato.nome_fantasia}' (CNPJ/CPF: {contrato.documento}) está próximo do vencimento em {context['dias_restantes']} dias (Data de Validade: {contrato.data_validade.strftime('%d/%m/%Y')}).",
                from_email=settings.EMAIL_HOST_USER,
                to=destinatarios_finais # Lista de destinatários únicos
            )
            email.attach_alternative(html_content, "text/html")

            # Enviar e-mail
            email.send()
            print(f"Lembrete enviado para o contrato {contrato.id} - {contrato.nome_fantasia}. Destinatários: {', '.join(destinatarios_finais)}")
            
            contratos_com_email_enviado.append(contrato.id) # Adiciona ID para atualização posterior

        except Exception as e:
            print(f"Erro ao enviar e-mail para o contrato {contrato.id} - {contrato.nome_fantasia}: {e}")

    # Atualizar apenas os contratos para os quais o e-mail foi realmente enviado
    if contratos_com_email_enviado:
        Contrato.objects.filter(id__in=contratos_com_email_enviado).update(email_enviado=True)
        print(f"Total de {len(contratos_com_email_enviado)} contratos marcados como 'e-mail enviado'.")
    else:
        print("Nenhum contrato foi atualizado como 'e-mail enviado'.")

    print("Verificação de lembretes de vencimento concluída.")