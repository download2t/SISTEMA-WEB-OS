from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Contrato
from .forms import ContratoForm
from datetime import timedelta, timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import has_permission
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.utils.timezone import now
from django.shortcuts import render
from datetime import timedelta
from .models import Contrato
from django.contrib.auth.models import Group
from django.http import HttpResponse
from reportlab.platypus import Table, TableStyle # type: ignore
from django.contrib import messages
from reportlab.pdfgen import canvas # type: ignore
from django.utils import timezone
from reportlab.lib import colors # type: ignore
from reportlab.lib.pagesizes import landscape, letter # type: ignore
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from reportlab.lib.units import inch # type: ignore
from docx import Document # type: ignore
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse



def listar_contratos(request):
    contratos = Contrato.objects.all()

    # Obtendo parâmetros da requisição
    tipo_data = request.GET.get("tipo_data", "assinatura")  # "assinatura" por padrão
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    razao_social = request.GET.get("razao_social", "").strip()
    grupo_id = request.GET.get("grupo")
    status = request.GET.get("status")

    # Filtro por Data
    if data_inicio and data_fim:
        if tipo_data == "assinatura":
            contratos = contratos.filter(data_assinatura__range=[data_inicio, data_fim])
        elif tipo_data == "validade":
            contratos = contratos.filter(data_validade__range=[data_inicio, data_fim])

    # Filtro por Razão Social ou Nome Fantasia (busca parcial)
    if razao_social:
        contratos = contratos.filter(
            nome_fantasia__icontains=razao_social
        ) | contratos.filter(
            razao_social__icontains=razao_social
        )

    # Filtro por Grupo
    if grupo_id:
        contratos = contratos.filter(grupo_responsavel=grupo_id)

    # Filtro por Status (ativo, inativo, vencido ou vencendo)
    hoje = now().date()
    if status == "ativo":
        contratos = contratos.filter(ativo=True)  # Alterado de "status" para "ativo"
    elif status == "inativo":
        contratos = contratos.filter(ativo=False)  # Alterado de "status" para "ativo"
    elif status == "vencido":
        contratos = contratos.filter(data_validade__lt=hoje)
    elif status == "vencendo":
        data_limite = hoje + timedelta(days=30)
        contratos = contratos.filter(data_validade__range=[hoje, data_limite])

    # Pegando todos os grupos para exibir no filtro
    grupos = Group.objects.all()

    context = {
        "contratos": contratos,
        "grupos": grupos,
        "tipo_data": tipo_data,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "razao_social": razao_social,
        "grupo": grupo_id,
        "status": status,
    }

    return render(request, "contratos/listar_contratos.html", context)


def has_permission_contratos(user):
    # Verifica se o usuário está autenticado e é staff ou pertence aos grupos "ADMIN" ou "LIDERANÇA"
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['ADMINISTRATIVO', 'ALMOXARIFADO','ADMIN','COMPRAS',
                                                            'COMERCIAL','GOVERNANÇA','LIDERANÇA','TI','RESERVAS','RECEPÇÃO']).exists())

@login_required
@user_passes_test(has_permission_contratos, login_url='403')  # Garantindo que o usuário tenha permissão
def criar_contrato(request):
    """ Cria um novo contrato """
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contrato criado com sucesso!")
            return redirect('listar_contratos')
    else:
        form = ContratoForm()
    
    return render(request, 'contratos/criar_contrato.html', {'form': form, 'titulo': 'Criar Contrato'})

@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def editar_contrato(request, contrato_id):
    """ Edita um contrato existente """
    contrato = get_object_or_404(Contrato, id=contrato_id)

    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            messages.success(request, "Contrato atualizado com sucesso!")
            return redirect('listar_contratos')
    else:
        form = ContratoForm(instance=contrato)
    
    return render(request, 'contratos/editar_contrato.html', {'form': form, 'titulo': 'Editar Contrato'})

@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def inativar_contrato(request, contrato_id):
    """ Inativa um contrato existente (não exclui o contrato, apenas marca como inativo) """
    contrato = get_object_or_404(Contrato, id=contrato_id)
    
    # Inativa o contrato
    contrato.ativo = False
    contrato.save()

    # Mensagem de sucesso
    messages.success(request, "Contrato inativado com sucesso!")

    return redirect('listar_contratos')

def ativar_contrato(request, contrato_id):
    """ Ativa um contrato existente (não exclui o contrato, apenas marca como ativo) """
    contrato = get_object_or_404(Contrato, id=contrato_id)
    
    # Ativa o contrato
    contrato.ativo = True
    contrato.save()

    # Mensagem de sucesso
    messages.success(request, "Contrato ativado com sucesso!")

    return redirect('listar_contratos')

def contratos_vencendo(request):
    hoje = now().date()
    limite_vencimento = hoje + timedelta(days=30)
    contratos = Contrato.objects.filter(ativo=True, data_validade__lte=limite_vencimento, data_validade__gte=hoje)
    
    return render(request, 'contratos/listar_contratos.html', {
        'contratos': contratos,
        'titulo_pagina': 'Contratos Vencendo'
    })

####################################### RELATÓRIOS #######################################

@login_required
@user_passes_test(has_permission, login_url='403')
def listar_contratos_rel(request):
    contratos = Contrato.objects.all()
    grupos = Group.objects.all()
    
    # Filtros
    razao_social = request.GET.get('razao_social')
    nome_fantasia = request.GET.get('nome_fantasia')
    documento = request.GET.get('documento')
    grupo = request.GET.get('grupo')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if razao_social:
        contratos = contratos.filter(razao_social__icontains=razao_social)
    if nome_fantasia:
        contratos = contratos.filter(nome_fantasia__icontains=nome_fantasia)
    if documento:
        contratos = contratos.filter(documento__icontains=documento)
    if grupo:
        contratos = contratos.filter(grupo_responsavel_id=grupo)
    if data_inicio:
        contratos = contratos.filter(data_assinatura__gte=data_inicio)
    if data_fim:
        contratos = contratos.filter(data_assinatura__lte=data_fim)

    return render(request, 'contratos/relatorios.html', {
        'contratos': contratos,
        'grupos': grupos,
    })

def abreviar_texto(texto, max_length):
    return texto if len(texto) <= max_length else texto[:max_length - 3] + "..."

def generate_word(request):
    contratos = Contrato.objects.all()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="relatorio_contratos.docx"'

    document = Document()
    document.add_heading('Relatório de Contratos', 0)

    for contrato in contratos:
        document.add_paragraph(f"Razão Social: {contrato.razao_social} | Nome Fantasia: {contrato.nome_fantasia} | Documento: {contrato.documento}")
        document.add_paragraph(f"Telefone: {contrato.telefone} | E-mail: {contrato.email}")
        document.add_paragraph(f"Data de Assinatura: {contrato.data_assinatura.strftime('%d/%m/%Y')} | Data de Validade: {contrato.data_validade.strftime('%d/%m/%Y')}")
        document.add_paragraph(f"Grupo Responsável: {contrato.grupo_responsavel.name} | Valor: {contrato.valor} | Ativo: {'Sim' if contrato.ativo else 'Não'}")
        document.add_paragraph(f"Descrição: {contrato.descricao or ''}")
        document.add_paragraph("_" * 100)

    document.save(response)
    return response

def generate_excel(request):
    contratos = Contrato.objects.all()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="relatorio_contratos.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contratos"

    # Cabeçalho
    headers = ['Razão Social', 'Nome Fantasia', 'Documento', 'Telefone', 'E-mail', 'Assinatura', 'Validade', 'Grupo', 'Valor', 'Ativo', 'Descrição']
    ws.append(headers)

    for contrato in contratos:
        ws.append([
            contrato.razao_social,
            contrato.nome_fantasia,
            contrato.documento,
            contrato.telefone,
            contrato.email,
            contrato.data_assinatura.strftime('%d/%m/%Y'),
            contrato.data_validade.strftime('%d/%m/%Y'),
            contrato.grupo_responsavel.name,
            contrato.valor,
            'Sim' if contrato.ativo else 'Não',
            contrato.descricao or '',
        ])

    for col_num, column_title in enumerate(headers, 1):
        column_letter = get_column_letter(col_num)
        ws.column_dimensions[column_letter].auto_size = True

    wb.save(response)
    return response

def gerar_relatorio_pdf(request):
    contratos = Contrato.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_contratos.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))

    largura_pagina, altura_pagina = landscape(letter)
    margem = 5  # Margem lateral
    altura_cabecalho = 70  # Espaço reservado para o cabeçalho
    altura_rodape = 20  # Espaço reservado para o rodapé
    linha_inicial = altura_pagina - altura_cabecalho
    linha_final = altura_rodape + 20  # Linha onde o rodapé começa

    def desenhar_cabecalho(pagina_atual, total_paginas):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margem, altura_pagina - 30, "Relatório de Contratos")
        pdf.setFont("Helvetica", 10)
        if request.user.is_authenticated:
            usuario_info = f"{request.user.first_name} {request.user.last_name} (ID: {request.user.id})"
        else:
            usuario_info = "Usuário Desconhecido"
        pdf.drawString(margem, altura_pagina - 70, f"Gerado por: {usuario_info}")
        pdf.drawRightString(largura_pagina - margem, altura_pagina - 30, f"Página {pagina_atual} de {total_paginas}")

    def desenhar_rodape():
        """Desenha o rodapé em cada página."""
        data_geracao = now().strftime('%d/%m/%Y %H:%M:%S')
        pdf.setFont("Helvetica", 9)
        pdf.drawString(margem, 30, f"Data/Hora: {data_geracao}")

    def desenhar_tabela(dados, y_pos):
        """Desenha uma tabela na posição y_pos."""
        table = Table(dados, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
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
        largura_tabela * 0.25,  # Coluna "Nome Fantasia"
        largura_tabela * 0.1,   # Coluna "Documento"
        largura_tabela * 0.1,   # Coluna "Telefone"
        largura_tabela * 0.2,  # Coluna "E-mail"
        largura_tabela * 0.08,   # Coluna "Data de Validade"
        largura_tabela * 0.1,   # Coluna "Grupo"
        largura_tabela * 0.11,   # Coluna "Valor"
        largura_tabela * 0.06,  # Coluna "Status"
    ]

    # Cabeçalho da tabela
    cabecalho_tabela = [["Nome Fantasia", "Documento", "Telefone", "E-mail", "Validade", "Grupo", "Valor", "Status"]]
    data = []
    for contrato in contratos:
        data.append([
            contrato.nome_fantasia,
            contrato.documento,
            contrato.telefone,
            contrato.email,
            contrato.data_validade.strftime("%d/%m/%Y"),
            contrato.grupo_responsavel.name,
            f'R$ {contrato.valor:.2f}', 
            'ATIVO' if contrato.ativo else 'INATIVO',
        ])

    # Limitar para 25 itens por página
    itens_por_pagina = 25
    paginas = [data[i:i + itens_por_pagina] for i in range(0, len(data), itens_por_pagina)]

    total_paginas = len(paginas)
    for i, pagina in enumerate(paginas):
        desenhar_cabecalho(i + 1, total_paginas)

        # Adicionar o cabeçalho da tabela a cada página
        pagina_com_cabecalho = cabecalho_tabela + pagina
        y_pos = linha_inicial - (len(pagina_com_cabecalho) * 20)
        desenhar_tabela(pagina_com_cabecalho, y_pos)

        desenhar_rodape()

        if i < len(paginas) - 1:
            pdf.showPage()  # Adicionar nova página

    pdf.save()
    return response



