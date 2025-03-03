# myapp/tasks.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Contrato

def verificar_contratos_vencendo():
    # Data de hoje
    hoje = timezone.now()

    # Data limite para vencimento de contratos (30 dias)
    data_limite = hoje + timezone.timedelta(days=30)

    # Filtra contratos com data de validade menor que a data limite e que não tiveram e-mail enviado
    contratos_a_vencer = Contrato.objects.filter(data_validade__lte=data_limite, email_enviado=False)

    for contrato in contratos_a_vencer:
        try:
            # Envia o e-mail de lembrete para um endereço fixo
            send_mail(
                'Lembrete de Vencimento de Contrato',
                f'O contrato {contrato.nome_fantasia} está próximo do vencimento.',
                settings.EMAIL_HOST_USER,
                ['ti@sanmahotel.com.br'],  # E-mail fixo para onde será enviado
                fail_silently=False,
            )
            
            # Marca o contrato como e-mail enviado
            contrato.email_enviado = True
            contrato.save()

            print(f'E-mail de lembrete enviado para financeiro@sanmahotel.com.br sobre o contrato de {contrato.nome_fantasia}')
        except Exception as e:
            print(f"Erro ao enviar e-mail para financeiro@sanmahotel.com.br sobre o contrato de {contrato.nome_fantasia}: {e}")

