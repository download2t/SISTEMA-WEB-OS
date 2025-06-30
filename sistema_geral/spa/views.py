from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Agendamento
from .forms import AgendamentoForm, EdicaoAgendamentoForm
from datetime import date
from django.utils import timezone
from datetime import date

def listar_spa(request):
    # Consulta inicial sem filtro de data
    agendamentos = Agendamento.objects.all().order_by('data', 'horario')
    
    # Obter todos os parâmetros de filtro
    status_filter = request.GET.get('status', '')
    nome_query = request.GET.get('nome', '').strip()
    quarto_query = request.GET.get('quarto', '').strip()
    data_inicio_query = request.GET.get('data_inicio', '')
    data_fim_query = request.GET.get('data_fim', '')

    # Aplicar filtros combinados
    if status_filter:
        agendamentos = agendamentos.filter(status=status_filter)
    else:
        # Filtro padrão: exclui cancelados se nenhum status for especificado
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

    # Contexto para template
    context = {
        'agendamentos': agendamentos,
        'status_choices': dict(Agendamento.STATUS_CHOICES),
        'status_filter': status_filter,
        'nome_query': nome_query,
        'quarto_query': quarto_query,
        'data_inicio_query': data_inicio_query,
        'data_fim_query': data_fim_query,
    }
    
    return render(request, 'spa/listar_spa.html', context)


def cadastro_spa(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.status = 'agendado'  # Status inicial
            agendamento.save()
            messages.success(request, 'Agendamento criado com sucesso!')
            return redirect('listar_spa')
    else:
        # Filtra apenas massagens ativas para novos agendamentos
        form = AgendamentoForm()
    
    return render(request, 'spa/cadastro_spa.html', {'form': form})

def editar_spa(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if request.method == 'POST':
        form = EdicaoAgendamentoForm(request.POST, instance=agendamento)
        try:
            if form.is_valid():
                agendamento_atualizado = form.save()
                
                # Mensagens de sucesso
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
            # Captura qualquer erro durante o salvamento
            messages.error(request, f'Erro ao salvar alterações: {str(e)}')
            # Adiciona os erros do formulário também
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
                    
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
    
    if agendamento.finalizar_servico():
        messages.success(request, 'Serviço marcado como realizado!')
    else:
        messages.error(request, 'Não foi possível finalizar o serviço.')
    
    return redirect('listar_spa')

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