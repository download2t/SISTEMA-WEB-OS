from .models import InstrucoesPDF
from .forms_instrucoes import InstrucoesPDFForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Restrição: membros do grupo LIDERANÇA, staff ou superusuário
def is_lideranca(user):
    return user.is_authenticated and (
        user.is_superuser or
        user.is_staff or
        user.groups.filter(name='LIDERANÇA').exists()
    )

@login_required
@user_passes_test(is_lideranca, login_url='403')
def cadastrar_instrucoes_pdf(request):
    obj, _ = InstrucoesPDF.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = InstrucoesPDFForm(request.POST)
        if form.is_valid():
            obj.texto = form.cleaned_data['instrucoes']
            obj.save()
            return redirect('listar_ramais')
    else:
        form = InstrucoesPDFForm(initial={'instrucoes': obj.texto})
    return render(request, 'ramais/cadastrar_instrucoes_pdf.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
import io
from xhtml2pdf import pisa
from .models import Ramal, Group
from .forms import RamalForm
from core.views import has_permission
from django.contrib import messages
from django.db.models import Q


# View para exportar PDF dos ramais (listão, sem agrupamento, respeitando filtro)
@login_required
def baixar_pdf_ramais(request):
    status = request.GET.get('status', 'todos')
    search = request.GET.get('search', '')

    # 1. Filtros
    ramais = Ramal.objects.all()
    if status != 'todos':
        if status == 'ativos':
            ramais = ramais.filter(ativo=True)
        elif status == 'inativos':
            ramais = ramais.filter(ativo=False)
    
    if search:
        ramais = ramais.filter(
            Q(numero_ramal__icontains=search)
            | Q(atendente__icontains=search)
            | Q(grupo__name__icontains=search)
            | Q(linha_completa__icontains=search)
            | Q(instrucoes_pdf__icontains=search)
        )
    
    # Ordenação (importante para as colunas fazerem sentido)
    ramais = ramais.order_by('numero_ramal')

    # Divide a lista de ramais em duas colunas
    meio = (len(ramais) + 1) // 2
    ramais_col1 = ramais[:meio]
    ramais_col2 = ramais[meio:]

    # Busca instruções do modelo único
    from .models import InstrucoesPDF
    instrucoes_obj = InstrucoesPDF.objects.first()
    instrucoes = instrucoes_obj.texto if instrucoes_obj else ''

    # 3. Renderização do HTML
    context = {
        'ramais_col1': ramais_col1,
        'ramais_col2': ramais_col2,
        'instrucoes': instrucoes,
    }
    html = render_to_string('ramais/pdf_ramais.html', context)

    # 4. Geração do PDF
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="lista_ramais.pdf"'
        return response
    
    return HttpResponse("Erro ao gerar PDF", status=400)

@login_required
def listar_ramais(request):
    status = request.GET.get('status', 'todos')  # Default 'todos'
    search = request.GET.get('search', '')

    ramais = Ramal.objects.all()

    if status != 'todos':
        if status == 'ativos':
            ramais = ramais.filter(ativo=True)
        elif status == 'inativos':
            ramais = ramais.filter(ativo=False)

    if search:
        ramais = ramais.filter(
            Q(numero_ramal__icontains=search)
            | Q(atendente__icontains=search)
            | Q(grupo__name__icontains=search)
            | Q(linha_completa__icontains=search)
            | Q(instrucoes_pdf__icontains=search)
        )

    ramais = ramais.order_by('numero_ramal')

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