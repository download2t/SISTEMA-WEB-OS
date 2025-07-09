# spa/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import date

from jsonschema import ValidationError # Import date for today's date
from .models import Agendamento, TipoMassagem
from .forms import AgendamentoForm, EdicaoAgendamentoForm, TipoMassagemForm

def listar_spa(request, filter_type=None): # Adicionado filter_type como argumento
    # Consulta inicial: Ordenar por data (asc) e horário (asc)
    agendamentos = Agendamento.objects.all().order_by('data', 'horario')
    
    # Títulos padrão
    titulo_pagina = 'Todos os Agendamentos'
    subtitulo_pagina = 'Visualize e gerencie todos os agendamentos do SPA.'

    # Aplica filtros baseados no tipo de filtro da URL (se houver)
    if filter_type == 'hoje':
        today = date.today()
        agendamentos = agendamentos.filter(data=today)
        titulo_pagina = 'Agendamentos para Hoje'
        subtitulo_pagina = f'Lista de agendamentos marcados para {today.strftime("%d/%m/%Y")}.'
    elif filter_type == 'cancelados':
        agendamentos = agendamentos.filter(status='cancelado').order_by('-data_cancelamento', 'data', 'horario')
        titulo_pagina = 'Agendamentos Cancelados'
        subtitulo_pagina = 'Todos os agendamentos que foram cancelados.'
    elif filter_type == 'realizados': # Use 'realizados' para consistência
        agendamentos = agendamentos.filter(status='realizado').order_by('-data', '-horario')
        titulo_pagina = 'Agendamentos Realizados'
        subtitulo_pagina = 'Todos os agendamentos que foram concluídos.'

    # Aplicar filtros da barra de busca (GET parameters)
    status_filter = request.GET.get('status', '')
    nome_query = request.GET.get('nome', '').strip()
    quarto_query = request.GET.get('quarto', '').strip()
    data_inicio_query = request.GET.get('data_inicio', '')
    data_fim_query = request.GET.get('data_fim', '')

    if status_filter:
        agendamentos = agendamentos.filter(status=status_filter)
    elif not filter_type: # Se não houver filtro de tipo (hoje/cancelados/realizados), exclui cancelados por padrão
        agendamentos = agendamentos.exclude(status='cancelado')
    
    if nome_query:
        agendamentos = agendamentos.filter(nome_hospede__icontains=nome_query)
    
    if quarto_query:
        agendamentos = agendamentos.filter(numero_quarto__icontains=quarto_query)
    
    if data_inicio_query:
        try:
            data_inicio = date.fromisoformat(data_inicio_query)
            agendamentos = agendamentos.filter(data__gte=data_inicio)
        except ValueError:
            pass 
    
    if data_fim_query:
        try:
            data_fim = date.fromisoformat(data_fim_query)
            agendamentos = agendamentos.filter(data__lte=data_fim)
        except ValueError:
            pass 

    context = {
        'agendamentos': agendamentos,
        'status_choices': dict(Agendamento.STATUS_CHOICES),
        'status_filter': status_filter,
        'nome_query': nome_query,
        'quarto_query': quarto_query,
        'data_inicio_query': data_inicio_query,
        'data_fim_query': data_fim_query,
        'titulo_pagina': titulo_pagina, 
        'subtitulo_pagina': subtitulo_pagina,
    }
    
    return render(request, 'spa/listar_spa.html', context)

# Mantenha as demais funções inalteradas, como cadastro_spa, editar_spa, etc.
def cadastro_spa(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.status = 'agendado'  # Initial status
            agendamento.save()
            messages.success(request, 'Agendamento criado com sucesso!')
            return redirect('listar_spa')
    else:
        form = AgendamentoForm()
    
    return render(request, 'spa/cadastro_spa.html', {'form': form})

def editar_spa(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if request.method == 'POST':
        form = EdicaoAgendamentoForm(request.POST, instance=agendamento)
        try:
            if form.is_valid():
                agendamento_atualizado = form.save()
                
                status_map = {
                    'realizado': ('success', 'Agendamento marcado como realizado com sucesso!'),
                    'cancelado': ('warning', 'Agendamento cancelado com sucesso!'),
                    'nao_compareceu': ('warning', 'Agendamento marcado como não compareceu!'),
                    'em_andamento': ('info', 'Agendamento marcado como em andamento!'),
                    'confirmado': ('success', 'Agendamento confirmado com sucesso!')
                }
                
                msg_type, msg_text = status_map.get(
                    agendamento_atualizado.status,
                    ('success', 'Agendamento atualizado com sucesso!')
                )
                
                getattr(messages, msg_type)(request, msg_text)
                return redirect('listar_spa')
                
        except Exception as e:
            messages.error(request, f'Erro ao salvar alterações: {str(e)}')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Campo "{field}": {error}')
                    
    else:
        form = EdicaoAgendamentoForm(instance=agendamento)

    return render(request, 'spa/editar_spa.html', {
        'form': form,
        'agendamento': agendamento,
        'editar': True
    })

def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '').strip()
        confirmado = request.POST.get('confirm_cancel', False)
        
        if not confirmado:
            messages.error(request, 'Você precisa confirmar o cancelamento marcando a caixa de confirmação.')
            return render(request, 'spa/cancelar_spa.html', {
                'agendamento': agendamento
            })
        
        if not motivo:
            messages.error(request, 'Por favor, informe o motivo do cancelamento.')
            return render(request, 'spa/cancelar_spa.html', {
                'agendamento': agendamento
            })
        
        try:
            agendamento.status = 'cancelado'
            agendamento.motivo_cancelamento = motivo
            agendamento.data_cancelamento = timezone.now()
            agendamento.save()
            
            messages.success(request, 'Agendamento cancelado com sucesso!')
            return redirect('listar_spa')
            
        except Exception as e:
            messages.error(request, f'Erro ao cancelar agendamento: {str(e)}')
            return render(request, 'spa/cancelar_spa.html', {
                'agendamento': agendamento
            })
    
    return render(request, 'spa/cancelar_spa.html', {
        'agendamento': agendamento
    })

def confirmar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if agendamento.confirmar():
        messages.success(request, 'Agendamento confirmado com sucesso!')
    else:
        messages.error(request, 'Não foi possível confirmar o agendamento.')
    
    return redirect('listar_spa')

def iniciar_servico(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if agendamento.iniciar_servico():
        messages.success(request, 'Serviço marcado como em andamento!')
    else:
        messages.error(request, 'Não foi possível iniciar o serviço.')
    
    return redirect('listar_spa')

def finalizar_servico(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if request.method == 'POST': # Garante que só processa via POST
        try:
            if agendamento.finalizar_servico():
                messages.success(request, 'Serviço marcado como realizado!')
            else:
                messages.error(request, 'Não foi possível finalizar o serviço.')
        except Exception as e:
            messages.error(request, f'Erro ao finalizar serviço: {str(e)}')
        return redirect('listar_spa')
    
    messages.warning(request, 'Ação de finalizar serviço requer submissão de formulário (POST).')
    return redirect('listar_spa') # Redireciona se for GET

def nao_compareceu(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if agendamento.registrar_nao_compareceu():
        messages.success(request, 'Registrado como não compareceu!')
    else:
        messages.error(request, 'Não foi possível registrar não comparecimento.')
    
    return redirect('listar_spa')

def reativar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if agendamento.reativar():
        messages.success(request, 'Agendamento reativado com sucesso!')
    else:
        messages.error(request, 'Não foi possível reativar o agendamento.')
    
    return redirect('listar_spa')

def relatorio_spa(request):
    # Para manter a estrutura atual que renderiza listar_spa.html:
    agendamentos = Agendamento.objects.all().order_by('data', 'horario')
    context = {
        'agendamentos': agendamentos,
        'status_choices': dict(Agendamento.STATUS_CHOICES),
        'titulo_pagina': 'Relatórios de Agendamentos',
        'subtitulo_pagina': 'Visualize todos os agendamentos registrados',
    }
    return render(request, 'spa/listar_spa.html', context)


# --- NOVAS FUNÇÕES PARA TipoMassagem ---

def listar_massagens(request):
    massagens = TipoMassagem.objects.all().order_by('nome')
    context = {
        'massagens': massagens,
        'titulo_pagina': 'Gestão de Massagens',
        'subtitulo_pagina': 'Visualize, crie e edite os tipos de massagens oferecidos.'
    }
    # CHANGE THIS LINE:
    return render(request, 'spa/massagem/listar_massagem.html', context) 

def criar_massagem(request):
    if request.method == 'POST':
        form = TipoMassagemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de massagem criado com sucesso!')
            return redirect('listar_massagens')
        else:
            # Exibir erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo "{field}": {error}')
    else:
        form = TipoMassagemForm()
    
    return render(request, 'spa/massagem/cadastro_massagem.html', {
        'form': form,
        'titulo_pagina': 'Criar Nova Massagem',
        'subtitulo_pagina': 'Adicione um novo tipo de massagem ao sistema.'
    })

def editar_massagem(request, pk):
    massagem = get_object_or_404(TipoMassagem, pk=pk)
    if request.method == 'POST':
        form = TipoMassagemForm(request.POST, instance=massagem)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Tipo de massagem atualizado com sucesso!')
                return redirect('listar_massagens')
            else:
                # Exibir erros do formulário
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Erro no campo "{field}": {error}')
        except ValidationError as e: # Captura ValidationError específico do clean() do modelo
            messages.error(request, f'Erro de validação: {e.message}')
        except Exception as e:
            messages.error(request, f'Erro ao salvar alterações: {str(e)}')
    else:
        form = TipoMassagemForm(instance=massagem)
    
    return render(request, 'spa/massagem/editar_massagem.html', {
        'form': form,
        'massagem': massagem,
        'titulo_pagina': 'Editar Massagem',
        'subtitulo_pagina': f'Editando: {massagem.nome}'
    })

def inativar_massagem(request, pk):
    massagem = get_object_or_404(TipoMassagem, pk=pk)
    if request.method == 'POST':
        # Ao invés de `massagem.delete()`, chamamos a validação e mudamos 'ativo'
        # O método delete() do modelo já faz o soft delete.
        # Precisamos simular o comportamento de validação do clean() antes de salvar.
        massagem.ativo = False
        try:
            massagem.full_clean() # Chama clean() do modelo para validação
            massagem.save()
            messages.success(request, f'Massagem "{massagem.nome}" inativada com sucesso.')
        except ValidationError as e:
            messages.error(request, f'Não foi possível inativar a massagem: {e.message}')
        except Exception as e:
            messages.error(request, f'Erro ao inativar massagem: {str(e)}')
    else:
        messages.warning(request, 'Ação de inativação requer uma requisição POST.')
    
    return redirect('listar_massagens')

def visualizar_massagem(request, pk):
    massagem = get_object_or_404(TipoMassagem, pk=pk)
    context = {
        'massagem': massagem,
        'titulo_pagina': 'Detalhes da Massagem',
        'subtitulo_pagina': f'Visualizando: {massagem.nome}'
    }
    return render(request, 'spa/massagem/visualizar_massagem.html', context)

def reativar_massagem(request, pk):
    massagem = get_object_or_404(TipoMassagem, pk=pk)
    if request.method == 'POST':
        massagem.ativo = True
        try:
            massagem.save() # Não precisa de full_clean aqui, pois não há validação para reativar
            messages.success(request, f'Massagem "{massagem.nome}" reativada com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao reativar massagem: {str(e)}')
    else:
        messages.warning(request, 'Ação de reativação requer uma requisição POST.')
    
    return redirect('listar_massagens')