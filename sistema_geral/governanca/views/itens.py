from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from core.views import has_permission
from governanca.forms import ItemLavanderiaForm
from governanca.models import ItemLavanderia
from django.db.models import Q



# Create your views here.
@login_required
def selecionarGov(request): # index de governanca
    return render(request, 'governanca/governanca_index.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test


# Criar um novo ItemLavanderia
@login_required
@user_passes_test(has_permission, login_url='403')
def create_item_lavanderia(request):
    form = ItemLavanderiaForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Item de lavanderia criado com sucesso!')
            return redirect(reverse('item_lavanderia_list'))  # Redireciona para a lista de itens
        else:
            messages.error(request, 'Erro ao criar o item de lavanderia. Verifique os dados fornecidos.')

    return render(request, 'governanca/itens/criar_item.html', {'form': form})

# Editar um ItemLavanderia existente
@login_required
@user_passes_test(has_permission, login_url='403')
def update_item_lavanderia(request, item_id):
    item = get_object_or_404(ItemLavanderia, id=item_id)
    form = ItemLavanderiaForm(request.POST or None, instance=item)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Item de lavanderia atualizado com sucesso!')
            return redirect(reverse('item_lavanderia_list'))  # Redireciona para a lista de itens
        else:
            messages.error(request, 'Erro ao atualizar o item de lavanderia. Verifique os dados informados.')

    return render(request, 'governanca/itens/editar_item.html', {'form': form, 'item': item})



@login_required
@user_passes_test(has_permission, login_url='403')
def delete_item_lavanderia(request, item_id):
    item = get_object_or_404(ItemLavanderia, id=item_id)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item de lavanderia excluído com sucesso!')
        return redirect('item_lavanderia_list')

    return render(request, 'governanca/itens/excluir_item.html', {'item': item})


# View para listar os itens de lavanderia
@login_required
def list_item_lavanderia(request):
    search = request.GET.get('search', '').strip()

    if search:
        items = ItemLavanderia.objects.filter(
            Q(nome__icontains=search) | Q(valormedio__icontains=search)
        )
    else:
        items = ItemLavanderia.objects.all()

    context = {
        'itens': items,
        'request': request,
    }
    return render(request, 'governanca/itens/listar_itens.html', context)
