from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Senha, Categoria
from .forms import SenhaFormPrivado, SenhaFormPublica, CategoriaForm
from core.views import has_permission

# CRUD para Categorias

@login_required
def listar_categorias(request):
    search = request.GET.get('search', '')
    tipo = request.GET.get('tipo', 'todas')  # Captura o valor do filtro de tipo

    categorias = Categoria.objects.all()

    # Se houver busca, filtra as categorias por nome ou descrição
    if search:
        categorias = categorias.filter(
            Q(nome__icontains=search) | Q(descricao__icontains=search)
        )

    # Se o filtro for "coletiva", filtra as categorias coletivas
    if tipo == 'coletiva':
        categorias = categorias.filter(is_coletiva=True)  
    
    # Se o filtro for "pessoal", filtra as categorias pessoais do usuário logado
    elif tipo == 'pessoal':
        categorias = categorias.filter(is_coletiva=False, usuario=request.user)  

    # Se o filtro for "todas", mostra as categorias coletivas e as pessoais do usuário logado
    elif tipo == 'todas':
        categorias = categorias.filter(
            Q(is_coletiva=True) | Q(is_coletiva=False, usuario=request.user)  
        )

    categorias = categorias.order_by('nome')

    return render(request, 'banco_senhas/categorias/listar_categorias.html', {'categorias': categorias})

def pode_adicionar_categoria_publica(user):

    return user.is_staff or user.groups.filter(name__in=['ADMIN', 'LIDERANÇA']).exists()

@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, user=request.user)  # Passando o usuário logado
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user  # Atribui o usuário logado à categoria
            
            # Verifica se a categoria é pública (is_coletiva=True)
            if categoria.is_coletiva and not pode_adicionar_categoria_publica(request.user):
                messages.error(request, 'Você não tem permissão para adicionar categorias públicas.')
                return redirect('listar_categorias')  # Redireciona para a lista de categorias
            
            categoria.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('listar_categorias')  # Redireciona para a lista de categorias
        else:
            messages.error(request, 'Há erros no formulário. Por favor, corrija e tente novamente.')
    else:
        form = CategoriaForm(user=request.user)  # Passando o usuário logado para o formulário

    return render(request, 'banco_senhas/categorias/criar_categoria.html', {'form': form})

@login_required ## usado como popup em senhas redirecionando para senhas
def adicionar_categoria_senhas_privado(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, user=request.user)  # Passando o usuário logado
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user  # Atribui o usuário logado à categoria
            
            # Verifica se a categoria é pública (is_coletiva=True)
            if categoria.is_coletiva and not pode_adicionar_categoria_publica(request.user):
                messages.error(request, 'Você não tem permissão para adicionar categorias públicas.')
                return redirect('listar_categorias')  # Redireciona para a lista de categorias
            
            categoria.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            
            # Redirecionar para o formulário de cadastro de senha pessoal, passando as categorias
            return redirect('adicionar_senha_privada')  # Ou o nome correto da URL para o formulário de senha pessoal
            
    else:
        form = CategoriaForm(user=request.user)  # Passando o usuário logado para o formulário

    return render(request, 'banco_senhas/categorias/criar_categoria.html', {'form': form})

@login_required ## usado como popup em senhas redirecionando para senhas
def adicionar_categoria_senhas_publico(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, user=request.user)  # Passando o usuário logado
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user  # Atribui o usuário logado à categoria
            
            # Verifica se a categoria é pública (is_coletiva=True)
            if categoria.is_coletiva and not pode_adicionar_categoria_publica(request.user):
                messages.error(request, 'Você não tem permissão para adicionar categorias públicas.')
                return redirect('listar_categorias')  # Redireciona para a lista de categorias
            
            categoria.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            
            # Redirecionar para o formulário de cadastro de senha pessoal, passando as categorias
            return redirect('adicionar_senha_publica')  # Ou o nome correto da URL para o formulário de senha pessoal
            
    else:
        form = CategoriaForm(user=request.user)  # Passando o usuário logado para o formulário

    return render(request, 'banco_senhas/categorias/criar_categoria.html', {'form': form})


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    # Verifica se o usuário tem permissão para editar a categoria
    if not pode_excluir(request.user, categoria):
        messages.error(request, "Você não tem permissão para editar esta categoria.")
        return redirect('listar_categorias')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('listar_categorias')  # Redireciona para a lista de categorias
        else:
            messages.error(request, 'Há erros no formulário. Por favor, corrija e tente novamente.')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'banco_senhas/categorias/editar_categoria.html', {'form': form, 'categoria': categoria})


def pode_excluir(user, categoria):
    # Verifica se o usuário está autenticado
    if not user.is_authenticated:
        return False

    # Se a categoria for pública (is_coletiva=True), apenas ADMIN ou LIDERANÇA pode excluir
    if categoria.is_coletiva:
        return user.is_staff or user.groups.filter(name__in=['ADMIN', 'LIDERANÇA']).exists()

    # Se não for pública, o proprietário (usuário que criou) pode excluir
    return categoria.usuario == user


@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    # Verifica as permissões para exclusão
    if not pode_excluir(request.user, categoria):
        messages.error(request, "Você não tem permissão para excluir esta categoria.")
        return redirect('listar_categorias')

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('listar_categorias')

    return render(request, 'banco_senhas/categorias/excluir_categoria.html', {'categoria': categoria})




## CRUD PARA SENHAS


from django.db.models import Q

@login_required
def listar_senhas(request):
    # Pega o valor da busca e do tipo
    search = request.GET.get('search', '')  # Pega o valor da busca
    tipo = request.GET.get('tipo', 'todas')  # Pega o tipo de senha (coletiva, pessoal ou todas)

    # Inicializa o queryset de senhas
    senhas = Senha.objects.all()  # Inicia com todas as senhas

    # Filtrando por tipo (coletiva ou pessoal)
    if tipo == 'coletiva':
        # Senhas públicas (coletivas) visíveis para todos os usuários
        senhas = senhas.filter(is_coletiva=True)
    elif tipo == 'pessoal':
        # Senhas pessoais (privadas) do usuário logado
        senhas = senhas.filter(usuario=request.user, is_coletiva=False)
    elif tipo == 'todas':
        # Exibe senhas coletivas + pessoais do usuário logado
        senhas = senhas.filter(Q(is_coletiva=True) | Q(usuario=request.user, is_coletiva=False))

    # Filtro de busca adicional, se houver
    if search:
        # Buscando nos campos descricao, senha, user e categoria
        senhas = senhas.filter(
            Q(descricao__icontains=search) |  # Filtra por descrição
            Q(senha__icontains=search) |     # Filtra por senha
            Q(user__icontains=search) |      # Filtra pelo campo 'user' (login)
            Q(categoria__nome__icontains=search) |  # Filtra pela categoria (supondo que tenha um campo nome na categoria)
            Q(link__icontains=search)  # Filtra pelo campo link, se existir
        )

    # Passa a lista de senhas para o template
    return render(request, 'banco_senhas/senhas/listar_senhas.html', {'senhas': senhas})






@user_passes_test(has_permission, login_url='403')
@login_required
def excluir_senha(request, pk):
    senha = get_object_or_404(Senha, pk=pk, usuario=request.user)
    if request.method == 'POST':
        senha.delete()
        messages.success(request, 'Senha excluída com sucesso!')
        return redirect('listar_senhas')
    return render(request, 'banco_senhas/senhas/excluir_senha.html', {'senha': senha})


@login_required
def adicionar_senha_privada(request):
    # Filtra as categorias que não são coletivas e pertencem ao usuário
    categorias_privadas = Categoria.objects.filter(is_coletiva=False, usuario=request.user)

    if request.method == "POST":
        form = SenhaFormPrivado(request.POST)
        if form.is_valid():
            senha = form.save(commit=False)
            senha.usuario = request.user  # Define o usuário logado como o criador
            senha.is_coletiva = False  # Define que a senha é privada
            senha.save()
            return redirect("listar_senhas")  # Redireciona para a página de listar senhas após o sucesso
    else:
        form = SenhaFormPrivado()
        form.fields["categoria"].queryset = categorias_privadas

    return render(request, "banco_senhas/senhas/criar_senha_pessoal.html", {
        "form": form,
        "categorias": categorias_privadas  # Passa as categorias para o template
    })



@login_required
@user_passes_test(has_permission, login_url='403')
def adicionar_senha_publica(request):
    # Filtra as categorias onde is_coletiva = True (públicas)
    categorias_publicas = Categoria.objects.filter(is_coletiva=True)

    if request.method == "POST":
        form = SenhaFormPublica(request.POST)
        if form.is_valid():
            senha = form.save(commit=False)
            senha.usuario = request.user  # Define o usuário logado como o criador
            senha.is_coletiva = True  # Define que a senha é pública
            senha.save()
            return redirect("listar_senhas")  # Redireciona para a página de listar senhas após o sucesso
    else:
        # Passa as categorias públicas para o campo de categoria no formulário
        form = SenhaFormPublica()
        form.fields["categoria"].queryset = categorias_publicas

    return render(request, "banco_senhas/senhas/criar_senha_publica.html", {
        "form": form,
        "categorias": categorias_publicas  # Passa as categorias públicas para o template
    })


@login_required
def editar_senha_privada(request, senha_id):
    # Filtra a senha privada específica do usuário
    try:
        senha = Senha.objects.get(id=senha_id, usuario=request.user, is_coletiva=False)
    except Senha.DoesNotExist:
        return redirect("url_de_erro")  # Redireciona caso a senha não exista ou não pertença ao usuário

    # Obtém categorias privadas associadas ao usuário logado
    categorias_privadas = Categoria.objects.filter(is_coletiva=False, usuario=request.user)

    if request.method == "POST":
        form = SenhaFormPrivado(request.POST, instance=senha)
        if form.is_valid():
            senha = form.save(commit=False)
            senha.usuario = request.user  # Mantém o usuário logado como o criador
            senha.is_coletiva = False  # Mantém a senha como privada
            senha.save()
            return redirect("listar_senhas")  # Redireciona para a lista de senhas após salvar
    else:
        form = SenhaFormPrivado(instance=senha)
        form.fields["categoria"].queryset = categorias_privadas  # Passa categorias privadas para o formulário

    # Passa o formulário e as categorias para o template
    return render(request, "banco_senhas/senhas/editar_senha_pessoal.html", {
        "form": form,
        "categorias": categorias_privadas,  # Passa as categorias privadas para o template
    })

@login_required
@user_passes_test(has_permission, login_url='403')  # Garantindo que o usuário tenha permissão
def editar_senha_publica(request, senha_id):
    # Filtra a senha pública específica do usuário
    try:
        senha = Senha.objects.get(id=senha_id, usuario=request.user, is_coletiva=True)
    except Senha.DoesNotExist:
        return redirect("url_de_erro")  # Redireciona caso a senha não exista ou não pertença ao usuário

    # Filtra as categorias públicas para o usuário
    categorias_publicas = Categoria.objects.filter(is_coletiva=True)

    # Verifica se a requisição é POST
    if request.method == "POST":
        form = SenhaFormPublica(request.POST, instance=senha)
        if form.is_valid():
            senha = form.save(commit=False)
            senha.usuario = request.user  # Mantém o usuário logado como o criador
            senha.is_coletiva = True  # Mantém a senha como pública
            senha.save()
            return redirect("listar_senhas")  # Redireciona para a lista de senhas após salvar
    else:
        # Caso contrário, preenche o formulário com os dados da senha
        form = SenhaFormPublica(instance=senha)
        form.fields["categoria"].queryset = categorias_publicas

    # Renderiza a página com o formulário
    return render(request, "banco_senhas/senhas/editar_senha_publica.html", {
        "form": form
    })


@login_required
def selecionar(request): # usado para selecionar senha pessoal ou publica ( cadastro )
    return render(request, 'banco_senhas/senhas/selecionar.html')