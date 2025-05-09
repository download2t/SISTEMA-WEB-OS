from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import Contrato

@shared_task
def verificar_contratos_vencendo():
    """ Verifica contratos que vencem em menos de 60 dias e envia lembretes automaticamente """
    hoje = timezone.now()
    data_limite = hoje + timezone.timedelta(days=60)

    contratos_a_vencer = Contrato.objects.filter(data_validade__lte=data_limite, email_enviado=False)

    if not contratos_a_vencer.exists():
        print("Nenhum contrato para enviar lembrete.")
        return

    for contrato in contratos_a_vencer:
        try:
            # Gerar conteúdo do e-mail usando template HTML
            context = {
                "contrato": contrato,
                "data_limite": data_limite,
            }
            html_content = render_to_string("contratos/lembrete_vencimento.html", context)

            # Configurar e-mail
            assunto = "Lembrete de Vencimento de Contrato"
            destinatarios = list(set([
                contrato.email,
                    "ti@sanmahotel.com.br",
                    "financeiro@sanmahotel.com.br",
                    "administracao@sanmahotel.com.br",
                      ]))

            email = EmailMultiAlternatives(
                subject=assunto,
                body=f"O contrato {contrato.nome_fantasia} está próximo do vencimento.",
                from_email=settings.EMAIL_HOST_USER,
                to=destinatarios
            )
            email.attach_alternative(html_content, "text/html")

            # Enviar e-mail
            email.send()

            # Marcar contrato como e-mail enviado
            contrato.email_enviado = True

        except Exception as e:
            print(f"Erro ao enviar e-mail para {contrato.nome_fantasia}: {e}")

    # Atualizar todos os contratos com um único `update` para otimizar performance
    contratos_a_vencer.update(email_enviado=True)

    print("Lembretes de vencimento de contrato enviados com sucesso!")
