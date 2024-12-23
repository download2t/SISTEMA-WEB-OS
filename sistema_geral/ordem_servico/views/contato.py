from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group, User
from ordem_servico.models import Contato
from ordem_servico.forms import ContatoForm
from core.views import has_permission





@login_required
@user_passes_test(has_permission, login_url='403')
def criar_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato criado com sucesso.')
            return redirect('listar_contatos')
        else:
            messages.error(request, 'Erro ao criar o contato. Verifique os dados.')
    else:
        form = ContatoForm()

    grupos = Group.objects.exclude(name__in=['LIDERANÇA', 'ADMIN'])
    usuarios = User.objects.filter(is_active=True)

    return render(request, 'contatos/criar_contato.html', {
        'form': form,
        'grupos': grupos,
        'usuarios': usuarios
    })

@login_required
@user_passes_test(has_permission, login_url='403')
def listar_contatos(request):
    search = request.GET.get('search', '')
    contatos = Contato.objects.filter(nome_responsavel__icontains=search) if search else Contato.objects.all()
    return render(request, 'contatos/listar_contatos.html', {'contatos': contatos})

@login_required
@user_passes_test(has_permission, login_url='403')
def visualizar_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    return render(request, 'contatos/visualizar_contato.html', {'contato': contato})

@login_required
@user_passes_test(has_permission, login_url='403')
def excluir_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    if request.method == 'POST':
        contato.delete()
        messages.success(request, 'Contato excluído com sucesso.')
        return redirect('listar_contatos')
    return render(request, 'contatos/excluir_contato.html', {'contato': contato})

@login_required
@user_passes_test(has_permission, login_url='403')
def editar_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato atualizado com sucesso.')
            return redirect('listar_contatos')
        else:
            messages.error(request, 'Erro ao atualizar o contato. Verifique os dados.')
    else:
        form = ContatoForm(instance=contato)

    grupos = Group.objects.exclude(name__in=['LIDERANÇA', 'ADMIN'])
    usuarios = User.objects.filter(is_active=True)

    return render(request, 'contatos/editar_contato.html', {
        'form': form,
        'contato': contato,
        'grupos': grupos,
        'usuarios': usuarios
    })
