from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from core.views import has_permission
from governanca.forms import RelatorioLavForm
from governanca.models import ItemLavanderia, ItemRelLavanderia
from governanca.models import RelatorioLav, ItemRelLavanderia
from django.utils import timezone
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import has_permission
import re


def formatar_valor(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        valor = re.sub(r'[^\d,.-]', '', valor) 
        valor = valor.replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return 0.0


@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
@transaction.atomic
def criar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioLavForm(request.POST)
        if form.is_valid():
            try:
                # Verifica se há pelo menos um item
                itens = request.POST.getlist('item_lavanderia')
                if not itens:
                    messages.error(request, 'É necessário adicionar pelo menos um item ao relatório.')
                    return render(request, 'governanca/relatorio/criar_relatorio.html', {
                        'form': form,
                        'itens_padrao': ItemLavanderia.objects.all(),
                        'post_data': request.POST,  # Passa os dados do POST de volta para o template
                    })

                # Verifica se há itens duplicados
                if len(itens) != len(set(itens)):
                    messages.error(request, 'Não é permitido adicionar itens duplicados ao relatório.')
                    return render(request, 'governanca/relatorio/criar_relatorio.html', {
                        'form': form,
                        'itens_padrao': ItemLavanderia.objects.all(),
                        'post_data': request.POST,  # Passa os dados do POST de volta para o template
                    })

                # Cria o relatório, mas não o salva ainda
                relatorio = form.save(commit=False)

                # Verifica se a data foi enviada no POST
                adata_str = request.POST.get('adata')
                if adata_str:
                    relatorio.adata = timezone.datetime.strptime(adata_str, '%Y-%m-%d')
                else:
                    relatorio.adata = timezone.now()

                # Corrige os valores com a função formatar_valor
                relatorio.vrTotal = formatar_valor(request.POST.get('vrTotal', '0'))
                relatorio.pesoTotal = formatar_valor(request.POST.get('pesoTotal', '0'))

                # Salva o relatório
                relatorio.save()

                # Chama a função para adicionar os itens ao relatório
                adicionar_itens_ao_relatorio(request, relatorio)

                # Redireciona após salvar com sucesso
                messages.success(request, 'Relatório criado com sucesso!')
                return redirect('listar_relatorios')

            except Exception as e:
                print(f"Erro ao criar relatório: {e}")
                messages.error(request, f'Erro ao criar o relatório: {str(e)}')
                return render(request, 'governanca/relatorio/criar_relatorio.html', {
                    'form': form,
                    'itens_padrao': ItemLavanderia.objects.all(),
                    'post_data': request.POST,  # Passa os dados do POST de volta para o template
                })
    else:
        form = RelatorioLavForm()

    # Carrega os itens padrão para o formulário
    itens_padrao = ItemLavanderia.objects.all()
    return render(request, 'governanca/relatorio/criar_relatorio.html', {
        'form': form,
        'itens_padrao': itens_padrao,
        'post_data': request.POST if request.method == 'POST' else None,  # Passa os dados do POST de volta para o template
    })


def adicionar_itens_ao_relatorio(request, relatorio):
    itens = request.POST.getlist('item_lavanderia')
    quantidades = request.POST.getlist('qtd_itens')
    relavagens = request.POST.getlist('qtd_relavagens')

    for i in range(len(itens)):
        item_id = int(itens[i])
        qtd_itens = int(quantidades[i])
        qtd_relavagens = int(relavagens[i])

        # Obtendo o item relacionado
        item = ItemLavanderia.objects.get(id=item_id)

        # Cálculo de relavagemkg
        relavagemkg_value = qtd_relavagens * item.pesokg

        # Criação do ItemRelLavanderia
        ItemRelLavanderia.objects.create(
            relatorio=relatorio,
            item_lavanderia=item,
            qtd_itens=qtd_itens,
            qtd_relavagens=qtd_relavagens,
            pesokg=item.pesokg,
            valormedio=item.valormedio,
            relavagemkg=relavagemkg_value
        )

def listar_relatorios(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio and data_fim:
        relatorios = RelatorioLav.objects.filter(adata__range=[parse_date(data_inicio), parse_date(data_fim)]).order_by('-adata')
    elif data_inicio:
        relatorios = RelatorioLav.objects.filter(adata__gte=parse_date(data_inicio)).order_by('-adata')
    elif data_fim:
        relatorios = RelatorioLav.objects.filter(adata__lte=parse_date(data_fim)).order_by('-adata')
    else:
        relatorios = RelatorioLav.objects.all().order_by('-adata')

    context = {
        'relatorios': relatorios
    }

    return render(request, 'governanca/relatorio/listar_relatorios.html', context)

def detalhar_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(RelatorioLav, id=relatorio_id)
    itens_relatorio = ItemRelLavanderia.objects.filter(relatorio=relatorio)

    context = {
        'relatorio': relatorio,
        'itens_relatorio': itens_relatorio
    }

    return render(request, 'governanca/relatorio/detalhes_relatorio.html', context)




def listar_relatorios(request):
    # Obtém as datas de início e fim do parâmetro de consulta, caso existam
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtra os relatórios conforme as datas, se fornecidas
    if data_inicio and data_fim:
        relatorios = RelatorioLav.objects.filter(adata__range=[parse_date(data_inicio), parse_date(data_fim)]).order_by('-adata')
    elif data_inicio:
        relatorios = RelatorioLav.objects.filter(adata__gte=parse_date(data_inicio)).order_by('-adata')
    elif data_fim:
        relatorios = RelatorioLav.objects.filter(adata__lte=parse_date(data_fim)).order_by('-adata')
    else:
        relatorios = RelatorioLav.objects.all().order_by('-adata')  # Retorna todos os relatórios se nenhuma data for fornecida

    context = {
        'relatorios': relatorios
    }

    return render(request, 'governanca/relatorio/listar_relatorios.html', context)




def detalhar_relatorio(request, relatorio_id):
    # Recupera o relatório e os itens relacionados
    relatorio = get_object_or_404(RelatorioLav, id=relatorio_id)
    itens_relatorio = ItemRelLavanderia.objects.filter(relatorio=relatorio)

    context = {
        'relatorio': relatorio,
        'itens_relatorio': itens_relatorio
    }

    return render(request, 'governanca/relatorio/detalhes_relatorio.html', context)
