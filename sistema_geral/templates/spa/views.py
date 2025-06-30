from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Agendamento, TipoMassagem
from .forms import AgendamentoForm, EdicaoAgendamentoForm

def listar_spa(request):
    # Filtra apenas massagens ativas para novos agendamentos
    status_filter = request.GET.get('status', 'todos')
    
    queryset = Agendamento.objects.all().order_by('data', 'horario')
    
    if status_filter != 'todos':
        queryset = queryset.filter(status=status_filter)
    
    context = {
        'agendamentos': queryset,
        'status_filter': status_filter,
        'status_choices': dict(Agendamento.STATUS_CHOICES),
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
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('listar_spa')
    else:
        form = EdicaoAgendamentoForm(instance=agendamento)
    
    return render(request, 'spa/editar_spa.html', {
        'form': form,
        'agendamento': agendamento
    })

def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '')
        if agendamento.cancelar(motivo):
            messages.success(request, 'Agendamento cancelado com sucesso!')
        else:
            messages.error(request, 'Não foi possível cancelar o agendamento.')
        return redirect('listar_spa')
    
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