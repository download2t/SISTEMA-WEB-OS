from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CanalForm, ListaCanaisForm, ListaCanais
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import has_permission
from .models import ListaCanais, Canal
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from io import BytesIO
import io


@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def criar_canal(request):
    if request.method == 'POST':
        form = CanalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Canal criado com sucesso!')
            return redirect('listar_canais')
        else:
            messages.error(request, 'Erro ao criar o canal. Verifique os dados fornecidos.')
    else:
        form = CanalForm()

    return render(request, 'canais/canais/criar_canal.html', {'form': form})

@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def editar_canal(request, canal_id):
    canal = get_object_or_404(Canal, id=canal_id)

    if request.method == 'POST':
        form = CanalForm(request.POST, instance=canal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Canal atualizado com sucesso!')
            return redirect('listar_canais')  # Redirecione para a lista de canais
        else:
            messages.error(request, 'Erro ao atualizar o canal. Verifique os dados informados.')
    else:
        form = CanalForm(instance=canal)
    
    return render(request, 'canais/canais/editar_canal.html', {'form': form, 'canal': canal})

@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def excluir_canal(request, canal_id):  # Verifique se está usando o nome correto do parâmetro
    canal = get_object_or_404(Canal, id=canal_id)

    if request.method == 'POST':
        canal.delete()
        messages.success(request, 'Canal excluído com sucesso!')
        return redirect('listar_canais')  # Redireciona após a exclusão

    return render(request, 'canais/canais/excluir_canal.html', {'canal': canal})

from django.db.models import Q  # Certifique-se de importar Q

@login_required
def listar_canais(request):
    # Obtém o termo de busca (se houver)
    search = request.GET.get('search', '').strip()

    # Filtra os canais com base na busca. Buscando por número ou título.
    if search:
        canais = Canal.objects.filter(
            Q(titulo__icontains=search) | Q(numero__icontains=search)
        )
    else:
        canais = Canal.objects.all()

    # Renderiza o template com os canais encontrados
    context = {
        'canais': canais,
        'request': request,
    }
    return render(request, 'canais/canais/listar_canais.html', context)






############################################ LISTAS ###################################################################



# View para listar listas de canais
def listar_listas(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Filtrar listas com base nas datas fornecidas
    if data_inicio and data_fim:
        listas = ListaCanais.objects.filter(data_criacao__gte=data_inicio, data_criacao__lte=data_fim)
    elif data_inicio:
        listas = ListaCanais.objects.filter(data_criacao__gte=data_inicio)
    elif data_fim:
        listas = ListaCanais.objects.filter(data_criacao__lte=data_fim)
    else:
        listas = ListaCanais.objects.all()
    
    return render(request, 'canais/listas/listar_listas.html', {'listas': listas})

# View para criar uma nova lista de canais
@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def criar_lista(request):
    if request.method == 'POST':
        form = ListaCanaisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lista de Canais criada com sucesso!')
            return redirect('listar_listas')
    else:
        form = ListaCanaisForm()

    return render(request, 'canais/listas/criar_lista.html', {'form': form})



# View para editar uma lista de canais existente
@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def editar_lista(request, lista_id):
    lista = get_object_or_404(ListaCanais, id=lista_id)
    
    if request.method == 'POST':
        form = ListaCanaisForm(request.POST, instance=lista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lista de Canais atualizada com sucesso!')
            return redirect('listar_listas')
    else:
        form = ListaCanaisForm(instance=lista)
    
    return render(request, 'canais/listas/editar_lista.html', {'form': form, 'lista': lista})





# View para excluir uma lista de canais
@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def excluir_lista(request, lista_id):
    lista = get_object_or_404(ListaCanais, id=lista_id)
    
    if request.method == 'POST':
        lista.delete()
        messages.success(request, 'Lista de Canais excluída com sucesso!')
        return redirect('listar_listas')
    
    return render(request, 'canais/listas/excluir_lista.html', {'lista': lista})


def ultima_lista(request):
    # Recupera a última lista criada (ordenada pela data de criação)
    ultima_lista = ListaCanais.objects.last()  # Retorna a última lista criada

    # Passa a última lista e seus canais para o template
    return render(request, 'canais/canais_tv.html', {'canais_tv': ultima_lista})




def download_pdf(request): ## utilizado dentro de listas/listas
    # Filtra a última lista criada (mais recente)
    lista = ListaCanais.objects.latest('data_criacao')

    # Criando uma resposta HTTP com tipo de conteúdo PDF
    buffer = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ultima_lista_de_canais_com_detalhes.pdf"'

    # Criando o PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Cabeçalho
    p.drawString(100, 750, "Lista atualizada de canais!")

    # Adicionando a informação da última lista
    y_position = 730
    p.drawString(100, y_position, f"Data de Criação da Lista: {lista.data_criacao}")
    y_position -= 20

    # Buscar canais associados à lista
    canais = lista.canais.all()  # Acessando os canais diretamente pela relação ManyToMany
    for canal in canais:
        p.drawString(120, y_position, f"Canal: {canal.numero} - {canal.titulo}")
        y_position -= 20

    p.showPage()
    p.save()

    # Prepara a resposta para o download do PDF
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response


def download_pdf_canais2(request):
    # Filtro de data, se fornecido
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Aplica o filtro das listas de canais conforme as datas
    if data_inicio and data_fim:
        listas = ListaCanais.objects.filter(data_criacao__gte=data_inicio, data_criacao__lte=data_fim)
    elif data_inicio:
        listas = ListaCanais.objects.filter(data_criacao__gte=data_inicio)
    elif data_fim:
        listas = ListaCanais.objects.filter(data_criacao__lte=data_fim)
    else:
        listas = ListaCanais.objects.all()

    # Criando uma resposta HTTP com tipo de conteúdo PDF
    buffer = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listas_de_canais_com_detalhes.pdf"'

    # Criando o PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Cabeçalho
    p.drawString(100, 750, "Listas de Canais")

    # Adicionando os itens das listas
    y_position = 730
    for lista in listas:
        p.drawString(100, y_position, f"Data de Criação da Lista: {lista.data_criacao}")
        y_position -= 20

        # Buscar canais associados à lista
        canais = lista.canais.all()  # Acessando os canais diretamente pela relação ManyToMany
        for canal in canais:
            p.drawString(120, y_position, f"Canal: {canal.numero} - {canal.titulo}")
            y_position -= 20

        y_position -= 10  # Espaço entre listas
        if y_position < 100:
            p.showPage()  # Nova página se o espaço acabar
            p.setFont("Helvetica", 12)
            y_position = 750

    p.showPage()
    p.save()

    # Prepara a resposta para o download do PDF
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response


def download_pdf_canais(request):
    # Filtro de data, se fornecido
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Aplica o filtro das listas de canais conforme as datas
    if data_inicio and data_fim:
        listas = ListaCanais.objects.filter(data_criacao__gte=data_inicio, data_criacao__lte=data_fim)
    elif data_inicio:
        listas = ListaCanais.objects.filter(data_criacao__gte=data_inicio)
    elif data_fim:
        listas = ListaCanais.objects.filter(data_criacao__lte=data_fim)
    else:
        listas = ListaCanais.objects.all()

    # Criando uma resposta HTTP com tipo de conteúdo PDF
    buffer = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listas_de_canais_com_detalhes.pdf"'

    # Criando o PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Cabeçalho
    p.drawString(100, 750, "Listas de Canais")

    # Adicionando os itens das listas
    y_position = 730
    for lista in listas:
        p.drawString(100, y_position, f"Data de Criação da Lista: {lista.data_criacao}")
        y_position -= 20

        # Buscar canais associados à lista
        canais = lista.canais.all()  # Acessando os canais diretamente pela relação ManyToMany
        for canal in canais:
            p.drawString(120, y_position, f"Canal: {canal.numero} - {canal.titulo}")
            y_position -= 20

        y_position -= 10  # Espaço entre listas
        if y_position < 100:
            p.showPage()  # Nova página se o espaço acabar
            p.setFont("Helvetica", 12)
            y_position = 750

    p.showPage()
    p.save()

    # Prepara a resposta para o download do PDF
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response