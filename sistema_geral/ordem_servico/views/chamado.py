from django.contrib.auth.decorators import login_required, user_passes_test   
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import  Q, Case, When, Value, IntegerField
from django.contrib.auth.models import Group
from django.utils.dateparse import parse_date
from ordem_servico.models import Chamado, Evidencia, GrupoTrabalho
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from ordem_servico.models import Contato
from ordem_servico.forms import MensagemForm
import requests # type: ignore

        
# Função para enviar a mensagem via API do WhatsApp
def enviar_mensagem_whatsapp(assunto, nome_usuario, data_hora, prioridade, grupo_responsavel):
    api_key = "sanma"  # Chave fixa da API
    
    # Tentar encontrar o contato associado ao grupo responsável
    try:
        contato = Contato.objects.get(grupo=grupo_responsavel)
        numero_destino = f"{contato.numero_telefone}@c.us"  # Número do responsável pelo grupo com o sufixo "@c.us"
    except Contato.DoesNotExist:
        print(f"Não foi encontrado um contato para o grupo {grupo_responsavel.name}.")
        return False

    # Garantir que a data está no formato desejado
    data_hora_formatada = timezone.localtime(timezone.now()).strftime('%d/%m/%Y às %H:%M')  # Formato: DD/MM/AAAA às HH:MM

    # URL da API
    url = "http://172.16.10.169:3000/client/sendMessage/sanma"
    mensagem = f"Uma nova OS foi aberta!\nTítulo: {assunto}\nPrioridade: {prioridade}\nCriado por: {nome_usuario}\nData: {data_hora_formatada}"

    payload = {
        "chatId": numero_destino,
        "contentType": "string",
        "content": mensagem
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        # Envia a requisição POST para a API do WhatsApp
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
            return True
        else:
            print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        # Em caso de erro na requisição
        print(f"Erro na requisição: {e}")
        return False


@login_required
def criar_chamado(request):
    # Filtra os grupos para incluir apenas "TI" e "MANUTENÇÃO"
    grupos = Group.objects.filter(name__in=['TI', 'MANUTENÇÃO'])
    grupos_usuario = request.user.groups.all()  # Grupos aos quais o usuário pertence
    
    # Ordena manualmente para garantir que "TI" venha primeiro
    grupos = sorted(grupos, key=lambda g: g.name != 'TI')

    # Obtém todos os grupos de trabalho disponíveis
    grupos_trabalho = GrupoTrabalho.objects.all()

    if request.method == 'POST':
        try:
            assunto = request.POST.get('assunto')
            descricao = request.POST.get('descricao')
            grupo_id = request.POST.get('grupo')
            grupo_trabalho_id = request.POST.get('grupo_trabalho')  # Obtém o ID do grupo de trabalho
            prioridade = request.POST.get('prioridade')

            print(f"grupo_id enviado: {grupo_id}")
            print(f"prioridade enviada: {prioridade}")
            print(f"grupo_trabalho_id enviado: {grupo_trabalho_id}")

            if grupo_id is None or grupo_id == "":
                raise ValueError("Nenhum grupo foi selecionado.")

            if prioridade not in ['Baixa', 'Média', 'Alta', 'Urgente']:
                raise ValueError("Prioridade inválida.")

            # Valida se o grupo de trabalho foi selecionado
            if grupo_trabalho_id is None or grupo_trabalho_id == "":
                raise ValueError("Nenhum grupo de trabalho foi selecionado.")

            grupo = Group.objects.get(id=grupo_id)  # Tenta encontrar o grupo com o ID
            grupo_trabalho = GrupoTrabalho.objects.get(id=grupo_trabalho_id)  # Tenta encontrar o grupo de trabalho com o ID
            status = "Aberto"

            # Cria o chamado com os dois campos: grupo responsável e grupos do usuário
            chamado = Chamado.objects.create(
                assunto=assunto,
                descricao=descricao,
                grupo_responsavel=grupo,
                grupo_trabalho=grupo_trabalho,  # Relaciona o grupo de trabalho ao chamado
                status=status,
                prioridade=prioridade,
                prioridade_cliente=prioridade,  # Copia a prioridade do campo para o cliente
                criado_por=request.user
            )

            # Relaciona os grupos do usuário ao chamado (campo ManyToMany)
            chamado.grupos_liberados.set(grupos_usuario)

            # Salva as evidências enviadas
            arquivos = request.FILES.getlist('evidencia')  # Obtém todos os arquivos enviados
            for arquivo in arquivos:
                Evidencia.objects.create(chamado=chamado, arquivo=arquivo)

            # Mensagem de sucesso
            messages.success(request, 'Chamado criado com sucesso!')

            # Enviar mensagem via WhatsApp com as informações do chamado
            nome_usuario = request.user.username
            data_hora = timezone.now().strftime('%Y-%m-%d %H:%M:%S')  # Data e hora atual formatada
            enviar_mensagem_whatsapp(assunto, nome_usuario, data_hora, prioridade, grupo)  # Envia a mensagem

            # Redireciona para a lista de chamados
            return redirect('listar_chamados')

        except Group.DoesNotExist:
            messages.error(request, 'Grupo selecionado não existe.')
        except GrupoTrabalho.DoesNotExist:
            messages.error(request, 'Grupo de trabalho selecionado não existe.')
        except ValueError as ve:
            messages.error(request, f'Erro: {ve}')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao criar o chamado: {e}')

    return render(request, 'ordem_servico/criar_chamado.html', {'grupos': grupos, 'grupos_trabalho': grupos_trabalho})


@login_required
def listar_chamados(request):
    grupos_usuario = request.user.groups.all()
    # All these conditions should be combined with an OR.
    chamados = Chamado.objects.filter(
        Q(grupo_responsavel__in=grupos_usuario) | 
        Q(criado_por=request.user) |
        Q(grupos_liberados__in=grupos_usuario)
    ).distinct() # `distinct()` is crucial here to avoid duplicate results

    # --- Filter by Multiple Statuses ---
    status_selecionados_str = request.GET.get('status', '')
    status_selecionados = [s.strip() for s in status_selecionados_str.split(',') if s.strip()]

    if status_selecionados:
        # for a literal status filter.
        chamados = chamados.filter(status__in=status_selecionados)

    # --- Filter by Search Term (ID, Subject, Description, Responsible Group, Creator) ---
    search_term = request.GET.get('search', '').strip() # Consistent variable name
    if search_term:
        # The search is applied *only* to the calls already filtered by visibility.
        chamados = chamados.filter(
            Q(id__icontains=search_term) |                  # Search by call ID
            Q(assunto__icontains=search_term) |             # Search in subject
            Q(descricao__icontains=search_term) |           # Search in description
            Q(grupo_responsavel__name__icontains=search_term) | # Search in responsible group name
            Q(criado_por__username__icontains=search_term) | # Search in creator's username
            Q(criado_por__first_name__icontains=search_term) | # Search in creator's first name
            Q(criado_por__last_name__icontains=search_term)   # Search in creator's last name
        ).distinct() # Keep distinct() here to prevent duplicates after implicit JOINs

    # --- Filter by Date (Start and End) ---
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date_obj = None
    end_date_obj = None

    if start_date_str:
        start_date_obj = parse_date(start_date_str)
        if start_date_obj:
            chamados = chamados.filter(data_abertura__date__gte=start_date_obj)

    if end_date_str:
        end_date_obj = parse_date(end_date_str)
        if end_date_obj:
            chamados = chamados.filter(data_abertura__date__lte=end_date_obj)
    
    # If both dates are provided and are the same, filter for that exact day.
    if start_date_obj and end_date_obj and start_date_obj == end_date_obj:
        chamados = chamados.filter(data_abertura__date=start_date_obj)

    # --- Order by Priority and Open Date ---
    chamados = chamados.annotate(
        prioridade_order=Case(
            When(prioridade='Urgente', then=Value(1)),
            When(prioridade='Alta', then=Value(2)),
            When(prioridade='Média', then=Value(3)),
            When(prioridade='Baixa', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        )
    ).order_by('prioridade_order', '-data_abertura')

    # --- Limit to 100 Calls (if no date filter is applied) ---
    if not start_date_str and not end_date_str:
        chamados = chamados[:100]

    # Display message only if, *after all filters*, no results are found.
    if not chamados.exists():
        messages.info(request, 'Nenhum chamado encontrado para os filtros aplicados.')
        
    # --- Prepare Context for Template ---
    context = {
        'chamados': chamados,
        'status_selecionados': status_selecionados,
        'search': search_term, # Pass the consistent search term to the template
        'start_date': start_date_str, # Pass original string for form field
        'end_date': end_date_str,     # Pass original string for form field
    }

    return render(request, 'ordem_servico/listar_chamados.html', context)
@login_required
def visualizar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    mensagens = chamado.mensagens.all()

    if request.method == 'POST':
        form = MensagemForm(request.POST, request.FILES)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.chamado = chamado
            mensagem.usuario = request.user
            mensagem.save()

            # Redireciona para a mesma página após salvar a mensagem
            return redirect('visualizar_chamado', id=chamado.id)
    else:
        form = MensagemForm()

    return render(request, 'ordem_servico/visualizar_chamado.html', {
        'chamado': chamado,
        'mensagens': mensagens,
        'form': form,
    })

@login_required
def encerrar_chamado(request, id):
    chamado = get_object_or_404(Chamado, pk=id)

    if request.method == 'POST':
        chamado.status = 'Concluído'
        chamado.data_conclusao = now()  # Adiciona a data e hora de encerramento
        chamado.save()

        # Adiciona a mensagem de sucesso
        messages.success(request, "Chamado encerrado com sucesso!")
        
        return redirect('listar_chamados')  # Redireciona para a página de listagem de chamados

    return render(request, 'ordem_servico/visualizar_chamado.html', {'chamado': chamado})

@login_required
def reabrir_chamado(request, pk):  # Use o mesmo nome definido na URL
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == 'Concluído':
        chamado.status = 'Aberto'
        chamado.data_conclusao = None
        chamado.save()
        messages.success(request, "Ordem de Serviço reaberta com sucesso!")
    return redirect('listar_chamados')


def chamado_atualizacao():
    try:
        # Destinatário fixo para o teste
        destinatario = 'mtduarte.b@gmail.com'

        # Envia o e-mail de atualização
        send_mail(
            'Atualização em seu chamado',  # Assunto do e-mail
            'Foi realizada uma nova atualização em seu chamado.',  # Corpo do e-mail
            settings.EMAIL_HOST_USER,  # Remetente
            [destinatario],  # Destinatário
            fail_silently=False,  # Se falhar, exibe a exceção
        )
        print(f"E-mail enviado com sucesso para {destinatario}.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    

@login_required
def meus_chamados(request):
    # Filtra apenas os chamados criados pelo usuário autenticado
    chamados = Chamado.objects.filter(criado_por=request.user)

    # Identifica a ação (filtro por status ou busca por usuário)
    action = request.GET.get('action')
    status_selecionados = []  # Inicializando para garantir que a variável seja definida
    search = ''

    if action == 'filter_status':
        # Filtro por múltiplos status
        status_selecionados = request.GET.get('status', '').split(',')
        if status_selecionados and status_selecionados != ['']:
            chamados = chamados.filter(status__in=status_selecionados)
            if not chamados.exists():
                messages.info(request, 'Nenhum chamado encontrado para os status selecionados.')
    elif action == 'search_user':
        # Busca por palavras-chave no título, descrição ou ID do chamado
        search = request.GET.get('search', '')
        if search:
            chamados = chamados.filter(
                Q(titulo__icontains=search) |
                Q(descricao__icontains=search) |
                Q(id__icontains=search)
            )
            if not chamados.exists():
                messages.info(request, 'Nenhum chamado encontrado para a busca realizada.')

    # Ordenação: 
    chamados = chamados.annotate(
        status_order=Case(
            When(status='Concluído', then=Value(1)),  # "Concluído" vai para o final
            default=Value(0),  # Outros status ficam antes
            output_field=IntegerField()
        ),
        prioridade_order=Case(
            When(prioridade='Urgente', then=Value(1)),
            When(prioridade='Alta', then=Value(2)),
            When(prioridade='Média', then=Value(3)),
            When(prioridade='Baixa', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        )
    ).order_by(
        'status_order',          # Ordena para colocar os "Concluídos" por último
        'prioridade_order',      # Ordena pelos valores de prioridade
        '-data_abertura'         # Para os não-concluídos, ordena do mais antigo para o mais recente
    )

    return render(request, 'ordem_servico/listar_chamados.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados,
        'search': search,
    })


@login_required
def chamados_abertos(request):
    grupos_usuario = request.user.groups.all()

    # Verifica se o usuário pertence aos grupos 'LIDERANÇA' ou 'ADMIN'
    is_lideranca_or_admin = any(grupo.name in ['LIDERANÇA', 'ADMIN'] for grupo in grupos_usuario)

    if is_lideranca_or_admin:
        # Usuário dos grupos 'LIDERANÇA' ou 'ADMIN' vê todos os chamados abertos (exceto os concluídos)
        chamados = Chamado.objects.exclude(status='Concluído')
    else:
        # Se o usuário não for 'LIDERANÇA' ou 'ADMIN', ele só vê chamados cujos grupos liberados correspondem aos grupos do usuário
        if grupos_usuario:
            chamados = Chamado.objects.filter(
                Q(grupos_liberados__in=grupos_usuario),  # Filtra chamados cujos grupos liberados correspondem ao grupo do usuário
                ~Q(status='Concluído')  # Exclui chamados com status 'Concluído'
            )
        else:
            chamados = Chamado.objects.none()  # Se o usuário não pertence a nenhum grupo, não mostra chamados

    # Identifica a ação (filtro por status ou busca por usuário)
    action = request.GET.get('action')

    if action == 'filter_status':
        # Filtro por múltiplos status dentro do contexto de chamados abertos
        status_selecionados = request.GET.get('status', '').split(',')
        if status_selecionados and status_selecionados != ['']:
            chamados = chamados.filter(status__in=status_selecionados)
            if not chamados.exists():
                messages.info(request, 'Nenhum chamado encontrado para os status selecionados.')
    elif action == 'search_user':
        # Filtro por busca no título, descrição ou usuário relacionado
        search = request.GET.get('search', '')
        if search:
            chamados = chamados.filter(
                Q(criado_por__username__icontains=search) |
                Q(criado_por__first_name__icontains=search) |
                Q(criado_por__last_name__icontains=search) |
                Q(id__icontains=search)
            )
            if not chamados.exists():
                messages.info(request, 'Nenhum chamado encontrado para a busca realizada.')

    # Ordenação por prioridade e data de abertura
    chamados = chamados.annotate(
        prioridade_order=Case(
            When(prioridade='Urgente', then=Value(1)),
            When(prioridade='Alta', then=Value(2)),
            When(prioridade='Média', then=Value(3)),
            When(prioridade='Baixa', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        )
    ).order_by(
        'prioridade_order',
        '-data_abertura'
    )

    return render(request, 'ordem_servico/listar_chamados.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados if action == 'filter_status' else [],
        'search': search if action == 'search_user' else '',
    })



@login_required
def chamados_encerrados(request):
    grupos_usuario = request.user.groups.all()

    # Filtra chamados onde os grupos liberados são iguais aos grupos do usuário e o status é 'Concluído'
    chamados = Chamado.objects.filter(
        Q(grupos_liberados__in=grupos_usuario),  # Filtra chamados cujos grupos liberados correspondem ao grupo do usuário
        status='Concluído'  # Considera apenas chamados com status 'Concluído'
    ).distinct()

    # Identifica a ação (filtro por status ou busca por usuário)
    action = request.GET.get('action')

    if action == 'filter_status':
        # Filtro por múltiplos status dentro do contexto de chamados encerrados
        status_selecionados = request.GET.get('status', '').split(',')
        if status_selecionados and status_selecionados != ['']:
            chamados = chamados.filter(status__in=status_selecionados)
            if not chamados.exists():
                messages.info(request, 'Nenhum chamado encontrado para os status selecionados.')
    elif action == 'search_user':
        # Filtro por busca no título, descrição ou usuário relacionado
        search = request.GET.get('search', '')
        if search:
            chamados = chamados.filter(
                Q(criado_por__username__icontains=search) |
                Q(criado_por__first_name__icontains=search) |
                Q(criado_por__last_name__icontains=search) |
                Q(id__icontains=search)
            )
            if not chamados.exists():
                messages.info(request, 'Nenhum chamado encontrado para a busca realizada.')

    # Ordenação por prioridade e data de abertura
    chamados = chamados.annotate(
        prioridade_order=Case(
            When(prioridade='Urgente', then=Value(1)),
            When(prioridade='Alta', then=Value(2)),
            When(prioridade='Média', then=Value(3)),
            When(prioridade='Baixa', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        )
    ).order_by(
        'prioridade_order',
        '-data_abertura'
    )

    return render(request, 'ordem_servico/listar_chamados.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados if action == 'filter_status' else [],
        'search': search if action == 'search_user' else '',
    })
 