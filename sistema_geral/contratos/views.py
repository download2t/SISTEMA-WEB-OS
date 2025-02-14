from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Contrato
from .forms import ContratoForm
from datetime import date


from datetime import date
from django.shortcuts import render
from .models import Contrato

def listar_contratos(request):
    """ Lista os contratos com filtros opcionais por intervalo de datas, razão social, nome fantasia e documento """
    contratos = Contrato.objects.all()
    today = date.today()  # Obtém a data de hoje

    # Obtém os parâmetros do formulário
    tipo_data = request.GET.get('tipo_data')  # 'assinatura' ou 'validade'
    data_inicio = request.GET.get('data_inicio')  # Data inicial do filtro
    data_fim = request.GET.get('data_fim')  # Data final do filtro
    razao_social = request.GET.get('razao_social', '').strip()  # Filtrar por Razão Social
    nome_fantasia = request.GET.get('nome_fantasia', '').strip()  # Filtrar por Nome Fantasia
    documento = request.GET.get('documento', '').strip()  # Filtrar por Documento

    # Filtra por datas se o tipo de data for válido
    if tipo_data in ['assinatura', 'validade']:
        campo_data = 'data_assinatura' if tipo_data == 'assinatura' else 'data_validade'
        
        if data_inicio:
            contratos = contratos.filter(**{f"{campo_data}__gte": data_inicio})
        if data_fim:
            contratos = contratos.filter(**{f"{campo_data}__lte": data_fim})

    # Filtra por Razão Social (busca parcial)
    if razao_social:
        contratos = contratos.filter(razao_social__icontains=razao_social)

    # Filtra por Nome Fantasia (busca parcial)
    if nome_fantasia:
        contratos = contratos.filter(nome_fantasia__icontains=nome_fantasia)

    # Filtra por Documento (busca exata)
    if documento:
        contratos = contratos.filter(documento=documento)

    return render(request, 'contratos/listar_contratos.html', {
        'contratos': contratos,
        'today': today,
        'tipo_data': tipo_data,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'razao_social': razao_social,
        'nome_fantasia': nome_fantasia,
        'documento': documento
    })




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
