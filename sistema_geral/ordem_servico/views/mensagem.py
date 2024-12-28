from django.contrib.auth.decorators import login_required, user_passes_test   
from django.shortcuts import render, redirect, get_object_or_404
from ordem_servico.models import Contato, Mensagem, Chamado
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from core.views import has_permission
from django.core.mail import send_mail

def testar_envio_email():
    try:
        send_mail(
            'Assunto Teste',  # Assunto do e-mail
            'Mensagem do teste',  # Corpo do e-mail
            settings.EMAIL_HOST_USER,  # Remetente
            ['ti@sanmahotel.com.br'],  # Destinatário
            fail_silently=False,  # Se falhar, exibe a exceção
        )
        print("E-mail de teste enviado.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

from django.core.exceptions import ObjectDoesNotExist

def enviar_mensagem(request, id):
    chamado = get_object_or_404(Chamado, id=id)

    if request.method == 'POST':
        texto = request.POST.get('mensagem')
        arquivo = request.FILES.get('arquivo')

        if texto:  # Cria a mensagem apenas se o texto for preenchido
            mensagem = Mensagem.objects.create(
                chamado=chamado,
                usuario=request.user,
                texto=texto,
                arquivo=arquivo
            )

            # Enviar e-mail para o contato responsável pelo grupo designado
            try:
                contato = Contato.objects.get(grupo=chamado.grupo_responsavel)
                contato_email = contato.usuario.email  # Obtém o e-mail do usuário vinculado ao contato
                
                # Formato do e-mail
                assunto = f"Atualização no Chamado #{chamado.id}"
                mensagem_email = (
                    f"Olá,\n\n"
                    f"Houve uma atualização no chamado #{chamado.id}.\n\n"
                    f"Mensagem:\n{texto}\n\n"
                    f"Atenciosamente,\nEquipe sanma."
                )

                send_mail(
                    assunto,
                    mensagem_email,
                    settings.EMAIL_HOST_USER,
                    [contato_email],
                    fail_silently=False
                )
                print(f"E-mail enviado para o contato responsável: {contato_email}")
            except ObjectDoesNotExist:
                print(f"Não foi encontrado um contato para o grupo {chamado.grupo_responsavel.name}.")
            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")

        return redirect('visualizar_chamado', id=id)  # Redireciona para a página do chamado

    return redirect('visualizar_chamado', id=id)


@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def adm_enviar_mensagem(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    destinatario_email = chamado.criado_por.email  

    print(f"Chamado: {chamado}")
    print(f"Destinatário email: {destinatario_email}")

    if not destinatario_email:
        messages.error(request, "O destinatário não possui um e-mail cadastrado.")
        print("Erro: Destinatário sem e-mail.")
        return redirect('visualizar_chamado', id=id)

    if request.method == 'POST':
        texto = request.POST.get('mensagem')
        arquivo = request.FILES.get('arquivo')
        
        if texto:  # Apenas cria a mensagem se o texto foi preenchido
            Mensagem.objects.create(
                chamado=chamado,
                usuario=request.user,
                texto=texto,
                arquivo=arquivo
            )
            
            # Enviar o e-mail
            assunto = f"Atualização no Chamado #{chamado.id}"
            mensagem = (
                f"Olá,\n\n"
                f"Houve uma atualização no chamado #{chamado.id}.\n\n"
                f"Mensagem:\n{texto}\n\n"
                f"Atenciosamente,\nEquipe sanma."
            )

            try:
                send_mail(
                    assunto,
                    mensagem,
                    settings.EMAIL_HOST_USER,
                    [destinatario_email],
                    fail_silently=False
                )
                messages.success(request, f"E-mail enviado com sucesso para {destinatario_email}.")
                print(f"E-mail enviado para {destinatario_email}")
            except Exception as e:
                import traceback
                print(f"Erro ao enviar e-mail: {e}")
                print(traceback.format_exc())   

        return redirect('adm_visualizar_chamado', id=id)

    # Adicionando um print para verificar se o método é GET
    print("Método GET recebido para adm_enviar_mensagem")
    return render(request, 'adm/enviar_mensagem.html', {'chamado': chamado})


