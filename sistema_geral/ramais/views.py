# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ramal
from django.contrib import messages
from .models import Ramal, Group
from .forms import RamalForm  
from core.views import has_permission
from django.db.models import Q

@login_required
def listar_ramais(request):
    # Obtenção dos parâmetros de busca
    status = request.GET.get('status', 'todos')  # Default 'todos'
    search = request.GET.get('search', '')

    # Filtragem dos ramais
    ramais = Ramal.objects.all()

    if status != 'todos':
        if status == 'ativos':
            ramais = ramais.filter(ativo=True)
        elif status == 'inativos':
            ramais = ramais.filter(ativo=False)

    if search:
        ramais = ramais.filter(
            Q(numero_ramal__icontains=search) | Q(atendente__icontains=search)
        )

    return render(request, 'ramais/listar_ramais.html', {'ramais': ramais})

@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
@login_required
def adicionar_ramal(request):
    # Filtra os grupos para incluir todos, exceto "ADMIN" e "LIDERANÇA"
    grupos = Group.objects.exclude(name__in=['ADMIN', 'LIDERANÇA'])

    if request.method == 'POST':
        form = RamalForm(request.POST)
        if form.is_valid():
            # Aqui podemos adicionar o grupo selecionado diretamente ao ramal, caso o form tenha um campo para isso
            form.save()
            return redirect('listar_ramais')  # Redireciona para a lista de ramais
    else:
        form = RamalForm()

    # Passa os grupos para o template, para que o usuário possa selecionar um grupo
    return render(request, 'ramais/criar_ramal.html', {'form': form, 'grupos': grupos})

@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
@login_required
def editar_ramal(request, pk):
    ramal = get_object_or_404(Ramal, pk=pk)
    grupos = Group.objects.all()  # Recupera todos os grupos disponíveis

    if request.method == "POST":
        form = RamalForm(request.POST, instance=ramal)

        if form.is_valid():
            form.save()
            # Adicionando mensagem de sucesso
            messages.success(request, 'Ramal atualizado com sucesso!')
            return redirect('listar_ramais')  # Redireciona para a página de lista de ramais
        else:
            # Se o formulário não for válido, renderiza a página com erros
            messages.error(request, 'Erro ao atualizar o ramal. Verifique os campos.')
    else:
        # Preenche o formulário com os dados atuais do ramal
        form = RamalForm(instance=ramal)

    return render(request, 'ramais/editar_ramal.html', {
        'ramal': ramal,
        'form': form,
        'grupos': grupos,
    })

@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
@login_required
def excluir_ramal(request, pk):
    ramal = get_object_or_404(Ramal, pk=pk)
    if request.method == 'POST':
        ramal.delete()
        return redirect('listar_ramais')
    return render(request, 'ramais/excluir_ramal.html', {'ramal': ramal})