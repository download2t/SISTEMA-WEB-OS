from django.contrib.auth.decorators import login_required, user_passes_test   
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import  Q, Case, When, Value, IntegerField
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib.pagesizes import landscape, letter # type: ignore
from django.contrib.auth.models import Group, User
from core.views import has_permission
from ordem_servico.models import Chamado
from reportlab.platypus import Table, TableStyle # type: ignore
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.contrib import messages
from reportlab.pdfgen import canvas # type: ignore
from django.utils import timezone
from reportlab.lib import colors # type: ignore
from django.conf import settings
from ordem_servico.forms import MensagemForm


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


@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
@login_required
def adm_listar_chamados(request):
    grupos_usuario = request.user.groups.all()

    # Filtrar chamados pelo grupo responsável ou criados pelo usuário
    chamados = Chamado.objects.filter(
        Q(grupo_responsavel__in=grupos_usuario) | Q(criado_por=request.user)
    ).distinct()

    # Filtro por status múltiplo
    status_selecionados = request.GET.get('status', '').split(',')
    if status_selecionados and status_selecionados != ['']:
        # Se "Aberto" for um dos status selecionados, vamos filtrar por todos os status exceto "Concluído"
        if 'Aberto' in status_selecionados:
            chamados = chamados.exclude(status='Concluído')  # Excluir os chamados "Concluído"
        else:
            chamados = chamados.filter(status__in=status_selecionados)

        if not chamados.exists():
            messages.info(request, 'Nenhum chamado encontrado para os status selecionados.')

    # Filtro por busca (grupo ou número do chamado)
    search = request.GET.get('search', '')
    if search:
        chamados = chamados.filter(
            Q(grupo_responsavel__name__icontains=search) |
            Q(id__icontains=search)
        ).distinct()
        if not chamados.exists():
            messages.info(request, 'Nenhum chamado encontrado para a busca realizada.')

    # Filtro por data
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            chamados = chamados.filter(data_abertura__date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            chamados = chamados.filter(data_abertura__date__lte=end_date)

    # Caso datas iguais
    if start_date and end_date and start_date == end_date:
        chamados = chamados.filter(data_abertura__date=start_date)

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
    ).order_by('prioridade_order', '-data_abertura')

    # Limitação de 100 chamados se nenhuma data estiver definida
    if not start_date and not end_date:
        chamados = chamados[:100]

    context = {
        'chamados': chamados,
        'status_selecionados': status_selecionados if status_selecionados != [''] else [],
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'adm_ordem_servico/listar.html', context)


@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def adm_visualizar_chamado(request, id):
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

    return render(request, 'adm_ordem_servico/visualizar.html', {
        'chamado': chamado,
        'mensagens': mensagens,
        'form': form,
    })

@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def atualizar_status(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    destinatario_email = chamado.criado_por.email  # Ou qualquer outro campo de relacionamento com o usuário responsável

    if request.method == 'POST':
        # Atualizar o status
        novo_status = request.POST.get('status')
        if novo_status in dict(Chamado.STATUS_CHOICES).keys():
            chamado.status = novo_status
        else:
            messages.error(request, 'Status inválido selecionado.')

        # Atualizar a prioridade
        nova_prioridade = request.POST.get('prioridade')
        if nova_prioridade in dict(Chamado.PRIORIDADE_CHOICES).keys():
            chamado.prioridade = nova_prioridade
        else:
            messages.error(request, 'Prioridade inválida selecionada.')

        # Atualizar o número do ticket, se aplicável
        numero_ticket = request.POST.get('numero_ticket')
        if novo_status == 'Encaminhado a TOTVS':
            if numero_ticket:  # Verificar se o número foi fornecido
                chamado.numero_ticket = numero_ticket
            else:
                messages.error(request, 'Por favor, insira o número do chamado para o status "Encaminhado a TOTVS".')

        # Atualizar a data de conclusão quando o status for "Concluído"
        if novo_status == 'Concluído':
            chamado.data_conclusao = timezone.now()  # Define a data de conclusão como a hora atual
        else:
            chamado.data_conclusao = None  # Se o status for alterado para algo diferente de "Concluído", define como nulo

        # Salvar as alterações apenas se todas as entradas forem válidas
        if (
            novo_status in dict(Chamado.STATUS_CHOICES).keys()
            and nova_prioridade in dict(Chamado.PRIORIDADE_CHOICES).keys()
        ):
            chamado.save()
            messages.success(
                request,
                f'Chamado atualizado com sucesso! Status definido como "{novo_status}" e prioridade como "{nova_prioridade}".'
            )

            # Enviar mensagem e e-mail informando a alteração do status
            if destinatario_email:
                assunto = f"Alteração no Chamado #{chamado.id} - Status Atualizado"
                mensagem = (
                    f"Olá,\n\n"
                    f"O status do seu chamado #{chamado.id} foi atualizado para: {novo_status}.\n\n"
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

            # Redirecionar para a página de listagem após salvar
            chamados = Chamado.objects.all()  # Exemplo de queryset para a página de listagem
            context = {'chamados': chamados}
            return render(request, 'adm_ordem_servico/listar.html', context)

    # Se houver erros, permanecer na mesma página e exibir as mensagens
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def adm_meus_chamados(request):
    # Filtra apenas os chamados criados pelo usuário autenticado
    chamados = Chamado.objects.filter(criado_por=request.user)

    # Identifica a ação (filtro por status ou busca por usuário)
    action = request.GET.get('action')

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

    return render(request, 'adm_ordem_servico/listar.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados if action == 'filter_status' else [],
        'search': search if action == 'search_user' else '',
    })

@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def adm_chamados_abertos(request):
    grupos_usuario = request.user.groups.all()

    # Verifica se o usuário pertence ao grupo "LIDERANÇA"
    eh_lideranca_ou_admin = grupos_usuario.filter(name__in=['LIDERANÇA', 'ADMIN']).exists()

    # Filtrar chamados:
    if eh_lideranca_ou_admin:
        # Se for da liderança, exibe todos os chamados abertos (exceto os concluídos)
        chamados = Chamado.objects.exclude(status='Concluído')  # Exclui chamados com status 'Concluído'
    elif grupos_usuario:
        # Caso contrário, filtra apenas os chamados do grupo do usuário
        chamados = Chamado.objects.filter(grupo_responsavel__in=grupos_usuario).exclude(status='Concluído')  # Exclui chamados com status 'Concluído'
    else:
        chamados = Chamado.objects.none()

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

    return render(request, 'adm_ordem_servico/listar.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados if action == 'filter_status' else [],
        'search': search if action == 'search_user' else '',
    })


@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def adm_chamados_encerrados(request):
    grupos_usuario = request.user.groups.all()

    # Verifica se o usuário pertence aos grupos 'LIDERANÇA' ou 'ADMIN'
    is_lideranca_or_admin = any(grupo.name in ['LIDERANÇA', 'ADMIN'] for grupo in grupos_usuario)

    # Se o usuário for do grupo 'LIDERANÇA' ou 'ADMIN', ele vê todos os chamados concluídos, sem filtrar pelos grupos
    if is_lideranca_or_admin:
        chamados = Chamado.objects.filter(status='Concluído')  # Vê todos os chamados concluídos
    else:
        # Filtra os chamados concluídos pelos grupos aos quais o usuário pertence
        if grupos_usuario:
            chamados = Chamado.objects.filter(grupo_responsavel__in=grupos_usuario, status='Concluído')
        else:
            chamados = Chamado.objects.none()

    # Identifica a ação (filtro por status ou busca por usuário)
    action = request.GET.get('action')

    if action == 'filter_status':
        # Filtro por múltiplos status dentro do contexto de chamados concluídos
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

    return render(request, 'adm_ordem_servico/listar.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados if action == 'filter_status' else [],
        'search': search if action == 'search_user' else '',
    })


@login_required
@user_passes_test(has_permission, login_url='403')  # Verifica se o usuário tem permissão
def adm_chamados_designados(request):
    grupos_usuario = request.user.groups.all()

    # Verifica se o usuário pertence ao grupo "LIDERANÇA"
    eh_lideranca_ou_admin = grupos_usuario.filter(name__in=['LIDERANÇA', 'ADMIN']).exists()


    # Filtrar chamados:
    if eh_lideranca_ou_admin:
        # Se for da liderança, exibe todos os chamados abertos
        chamados = Chamado.objects.filter(status='Conclúido')
    elif grupos_usuario:
        # Caso contrário, filtra apenas os chamados do grupo do usuário
        chamados = Chamado.objects.filter(grupo_responsavel__in=grupos_usuario, status='Aberto')
    else:
        chamados = Chamado.objects.none()

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

    return render(request, 'adm_ordem_servico/listar.html', {
        'chamados': chamados,
        'status_selecionados': status_selecionados if action == 'filter_status' else [],
        'search': search if action == 'search_user' else '',
    })

@user_passes_test(has_permission, login_url='403')  # Verifica se o usuário tem permissão
@login_required
def relatorio_chamados(request):
    # Filtros
    status_filter = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    grupo_filter = request.GET.get('grupo', '')
    responsavel_filter = request.GET.get('responsavel', '')

    # Base queryset
    chamados = Chamado.objects.all()

    # Filtro por Status (permite múltiplos status)
    if status_filter:
        status_list = status_filter.split(',')
        # Considerando "Aberto" e outros status, excluindo "Concluído" se "Aberto" for selecionado
        if 'Aberto' in status_list:
            chamados = chamados.filter(~Q(status='Concluído'))  # Exclui "Concluído"
        else:
            chamados = chamados.filter(status__in=status_list)

    # Filtro por Data
    if start_date:
        chamados = chamados.filter(data_abertura__gte=start_date)
    if end_date:
        chamados = chamados.filter(data_abertura__lte=end_date)

    # Filtro por Grupo
    if grupo_filter:
        chamados = chamados.filter(grupo_responsavel_id=grupo_filter)

    # Filtro por Responsável
    if responsavel_filter:
        chamados = chamados.filter(criado_por_id=responsavel_filter)

    # Enviar os dados para o template
    grupos = Group.objects.filter(name__in=['TI', 'MANUTENÇÃO'])  # Filtra para apenas os grupos TI e MANUTENÇÃO
    usuarios = User.objects.all()  # ou apenas os usuários relevantes

    return render(request, 'adm_ordem_servico/relatorios.html', {
        'chamados': chamados,
        'grupos': grupos,
        'usuarios': usuarios,
        'request': request,
    })


def abreviar_texto(texto, max_length):
    """Abrevia o texto se ele for maior que max_length."""
    return texto if len(texto) <= max_length else texto[:max_length - 3] + "..."
def gerar_relatorio_pdf(request):
    chamados = Chamado.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_chamados.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))

    largura_pagina, altura_pagina = landscape(letter)
    margem = 5  # Margem lateral
    altura_cabecalho = 80  # Espaço reservado para o cabeçalho
    altura_rodape = 20  # Espaço reservado para o rodapé
    linha_inicial = altura_pagina - altura_cabecalho
    linha_final = altura_rodape + 20  # Linha onde o rodapé começa

    def desenhar_cabecalho():
        """Desenha o cabeçalho na primeira página."""
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margem, altura_pagina - 50, "Relatório de Ordens de Serviço")
        pdf.setFont("Helvetica", 10)
        if request.user.is_authenticated:
            usuario_info = f"{request.user.first_name} {request.user.last_name} (ID: {request.user.id})"
        else:
            usuario_info = "Usuário Desconhecido"
        pdf.drawString(margem, altura_pagina - 70, f"Gerado por: {usuario_info}")

    def desenhar_rodape(pagina_atual, total_paginas):
        """Desenha o rodapé em cada página."""
        data_geracao = timezone.now().strftime('%d/%m/%Y %H:%M:%S')
        pdf.setFont("Helvetica", 9)
        pdf.drawString(margem, 30, f"Data/Hora: {data_geracao}")
        pdf.drawRightString(largura_pagina - margem, 30, f"Página {pagina_atual} de {total_paginas}")

    def desenhar_tabela(dados, y_pos):
        """Desenha uma tabela na posição y_pos."""
        table = Table(dados, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        table.wrapOn(pdf, largura_pagina - 2 * margem, altura_pagina)
        table.drawOn(pdf, margem, y_pos)

    # Configurar a largura das colunas
    largura_tabela = largura_pagina - 2 * margem
    col_widths = [
        50,                     # Coluna "ID"
        largura_tabela * 0.4,   # Coluna "Assunto"
        largura_tabela * 0.15,  # Coluna "Status"
        largura_tabela * 0.12,  # Coluna "Data Abertura"
        largura_tabela * 0.12,  # Coluna "Data Conclusão"
        largura_tabela * 0.15,  # Coluna "Responsável"
    ]

    # Cabeçalho da tabela
    cabecalho_tabela = [["TICKET", "Assunto", "Status", "Data Abertura", "Data Conclusão", "Responsável"]]
    data = []
    for chamado in chamados:
        data.append([
            chamado.id,
            abreviar_texto(chamado.assunto, 60),
            chamado.status,
            chamado.data_abertura.strftime("%d/%m/%Y"),
            chamado.data_conclusao.strftime("%d/%m/%Y") if chamado.data_conclusao else "N/A",
            chamado.grupo_responsavel.name,
        ])

    # Limitar para 25 itens por página
    itens_por_pagina = 25
    paginas = [data[i:i + itens_por_pagina] for i in range(0, len(data), itens_por_pagina)]

    total_paginas = len(paginas)
    for i, pagina in enumerate(paginas):
        if i == 0:  # Primeira página
            desenhar_cabecalho()

        # Adicionar o cabeçalho da tabela a cada página
        pagina_com_cabecalho = cabecalho_tabela + pagina
        y_pos = linha_inicial - (len(pagina_com_cabecalho) * 20)
        desenhar_tabela(pagina_com_cabecalho, y_pos)

        desenhar_rodape(i + 1, total_paginas)

        if i < len(paginas) - 1:
            pdf.showPage()  # Adicionar nova página

    pdf.save()
    return response
