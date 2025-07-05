from email.headerregistry import Group
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q  # Importando para consultas complexas
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, UsuarioForm  # Certifique-se de importar ambos os formulários
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse # Importe reverse para obter URLs por nome

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                if not user.is_active:
                    # Se o usuário estiver inativo, mostra a mensagem específica
                    messages.error(self.request, 'Usuário inativo. Por favor, entre em contato com o administrador.')
                else:
                    # Caso contrário, exibe a mensagem de erro padrão de senha incorreta
                    messages.error(self.request, 'Senha incorreta. Por favor, tente novamente.')
            else:
                # Caso o usuário não seja encontrado
                messages.error(self.request, 'Usuário não encontrado. Por favor, verifique o nome de usuário e tente novamente.')

        return super().form_invalid(form)


def has_permission(user):
    # Verifica se o usuário está autenticado e é staff ou pertence aos grupos "ADMIN" ou "LIDERANÇA"
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['ADMIN', 'LIDERANÇA']).exists())


def error_403_view(request):
    return render(request, 'core/403.html')

# Função que redireciona para a página de erro caso o usuário não tenha permissão
def permission_denied_view(request):
    return redirect('nao_autenticado')  # Redireciona para a página de erro

# Função para renderizar a página inicial, com redirecionamento para login se não autenticado
@login_required(login_url='login')
def home(request):
    return render(request, 'core/home.html')

# Página de erro de autenticação (403)
def nao_autenticado(request):
    return render(request, 'core/403.html')

# Página para usuários não logados
def nao_autenticado(request):
    return render(request, 'core/nao_autenticado.html')

# Classe LoginView personalizada para definir template de login
class LoginView(AuthLoginView):
    template_name = 'core/login.html'

# Página de confirmação de logout
@login_required
def logout_confirm(request):
    return render(request, 'core/logout_confirm.html')

# Seu_app/views.py



def custom_login(request):
    # Detecta se a requisição é AJAX (enviada pelo seu JavaScript)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # print(f"Usuário encontrado: {user.username}") # Mantenha para debug se quiser
            if user.is_active:
                login(request, user)
                
                if is_ajax:
                    # Para requisições AJAX, retorne JSON com a URL de redirecionamento
                    return JsonResponse({'success': True, 'redirect_url': reverse('home')})
                else:
                    # Para requisições normais, redirecione diretamente
                    return redirect('home')
            else:
                message_text = 'Usuário inativo. Por favor, entre em contato com o administrador.'
                if is_ajax:
                    return JsonResponse({'success': False, 'message': message_text}, status=400)
                else:
                    messages.error(request, message_text)
                    return redirect('login') # Redireciona de volta para a página de login
        else:
            message_text = 'Usuário ou senha incorretos. Por favor, tente novamente.'
            if is_ajax:
                return JsonResponse({'success': False, 'message': message_text}, status=400)
            else:
                messages.error(request, message_text)
                return redirect('login') # Redireciona de volta para a página de login
    
    # Se for uma requisição GET, renderiza o formulário de login
    return render(request, 'core/login.html') # Certifique-se de que o caminho do template está correto


# Função para alteração de senha do usuário
# Função para alteração de senha do usuário
@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após a alteração da senha
            messages.success(request, 'A senha foi alterada com sucesso!')
            # ALTERAÇÃO AQUI: Redireciona para a página 'home'
            return redirect('home')  # Certifique-se de que 'home' é o nome da sua URL de destino
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'core/accounts/alterar_senha.html', {'form': form})

# Função para cadastro de novos usuários
@login_required
@user_passes_test(has_permission, login_url='nao_autenticado')  # Redireciona se não for staff
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = 'is_staff' in request.POST
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('listar_usuarios')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/accounts/cadastrar_usuario.html', {'form': form})


@user_passes_test(lambda u: u.is_staff, login_url='nao_autenticado')  # Apenas staff pode acessar
def alterar_usuario(request, user_id):
    """
    View para alterar as informações de um usuário no sistema.
    """
    user = get_object_or_404(User, id=user_id)

    # Verifica se o usuário tem permissão para editar esse perfil
    if not request.user.is_superuser and request.user != user:
        messages.error(request, "Você não tem permissão para alterar este usuário.")
        return redirect('home')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)

            # Atualiza a senha, se informada
            password = form.cleaned_data.get('password')
            if password:
                updated_user.set_password(password)
                messages.info(request, "A senha foi alterada com sucesso.")

            # Atualiza o status de staff e ativo
            updated_user.is_staff = request.POST.get('is_staff') == 'on'
            updated_user.is_active = request.POST.get('is_active') == 'True'

            updated_user.save()

            # Atualiza os grupos do usuário
            selected_groups = request.POST.getlist('groups')
            user.groups.set(selected_groups)

            messages.success(request, "Usuário alterado com sucesso!")
            return redirect('listar_usuarios')  # Redireciona após salvar
        else:
            messages.error(request, "Erro ao alterar usuário. Verifique os dados.")
    else:
        form = UsuarioForm(instance=user)

    all_groups = Group.objects.all()
    user_groups = user.groups.all()

    context = {
        'form': form,
        'user': user,
        'all_groups': all_groups,
        'user_groups': user_groups,
    }
    return render(request, 'core/accounts/alterar_usuario.html', context)

# Função para listar todos os usuários
@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def listar_usuarios(request):
    status = request.GET.get('status', 'todos')  # Obtém o status da requisição GET
    search = request.GET.get('search', '')  # Obtém o valor do campo de pesquisa

    # Filtrando usuários por status
    if status == 'ativos':
        usuarios = User.objects.filter(is_active=True)
    elif status == 'inativos':
        usuarios = User.objects.filter(is_active=False)
    else:
        usuarios = User.objects.all()
    
    # Aplicando a pesquisa
    if search:
        # Usando Q para permitir busca por nome, email ou username
        usuarios = usuarios.filter(
            Q(username__icontains=search) | 
            Q(email__icontains=search) | 
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search)
        )
    
    return render(request, 'core/accounts/listar_usuarios.html', {'usuarios': usuarios})

@csrf_exempt
@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def ativar_usuario_toggle(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    # Impedir ativação de usuários já ativos
    if usuario.is_active:
        return JsonResponse({'success': False, 'message': 'Usuário já está ativo.'}, status=400)

    if request.method == 'POST':
        usuario.is_active = True
        usuario.save()
        return JsonResponse({'success': True, 'message': 'Usuário ativado com sucesso!'})
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)


@csrf_exempt
@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def desativar_usuario_toggle(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    # Impedir desativação de usuários staff
    if usuario.is_staff:
        return JsonResponse({'success': False, 'message': 'Usuários staff não podem ser inativados.'}, status=403)

    if request.method == 'POST':
        usuario.is_active = False
        usuario.save()
        return JsonResponse({'success': True, 'message': 'Usuário desativado com sucesso!'})
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)


@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def pesquisar_usuarios(request):
    status = request.GET.get('status', 'todos')
    search = request.GET.get('search', '')

    # Lógica para filtrar usuários
    if status == 'ativos':
        usuarios = User.objects.filter(is_active=True)
    elif status == 'inativos':
        usuarios = User.objects.filter(is_active=False)
    else:
        usuarios = User.objects.all()

    if search:
        usuarios = usuarios.filter(username__icontains=search)

    if request.is_ajax():  # Verifica se a requisição é AJAX
        return render(request, 'core/accounts/_listar_usuarios.html', {'usuarios': usuarios})

    return render(request, 'core/accounts/pesquisar_usuarios.html', {'usuarios': usuarios})

### GRUPOS #######################

@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def listar_grupos(request):
    search_query = request.GET.get('search', '')  # Recupera o termo de busca, se houver
    if search_query:
        # Filtra grupos pelo nome que contenha o termo de busca
        grupos_lista = Group.objects.filter(name__icontains=search_query)
    else:
        # Se não houver busca, retorna todos os grupos
        grupos_lista = Group.objects.all()
    
    paginator = Paginator(grupos_lista, 20)  # Paginação, 20 grupos por página
    page_number = request.GET.get('page')
    grupos = paginator.get_page(page_number)
    
    return render(request, 'core/grupos/listar_grupos.html', {'grupos': grupos, 'search_query': search_query})
@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def criar_grupo(request):
    if request.method == 'POST':
        nome_grupo = request.POST.get('nome')
        if nome_grupo:  # Verifica se o nome foi preenchido
            if not Group.objects.filter(name=nome_grupo).exists():
                Group.objects.create(name=nome_grupo)
                messages.success(request, 'Grupo criado com sucesso!')
                return redirect('listar_grupos')
            else:
                messages.error(request, 'Já existe um grupo com este nome!')
        else:
            messages.error(request, 'O nome do grupo é obrigatório.')
    return render(request, 'core/grupos/criar_grupo.html')

@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def editar_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)
    
    if request.method == 'POST':
        nome_grupo = request.POST.get('nome')
        if nome_grupo:  # Verifica se o nome foi preenchido
            if not Group.objects.filter(name=nome_grupo).exclude(id=grupo.id).exists():
                grupo.name = nome_grupo
                grupo.save()
                messages.success(request, 'Grupo editado com sucesso!')
                return redirect('listar_grupos')
            else:
                messages.error(request, 'Já existe um grupo com este nome!')
        else:
            messages.error(request, 'O nome do grupo é obrigatório.')

    return render(request, 'core/grupos/editar_grupo.html', {'grupo': grupo})

@login_required
@user_passes_test(has_permission, login_url='403')  # Redireciona para 403 se não for staff
def excluir_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)

    if request.method == 'POST':
        # Verifica se o grupo pode ser excluído (não tem usuários atribuídos a ele)
        if grupo.user_set.exists():
            messages.error(request, 'Não é possível excluir o grupo, pois existem usuários associados a ele.')
        else:
            grupo.delete()
            messages.success(request, 'Grupo excluído com sucesso!')
        return redirect('listar_grupos')

    return render(request, 'core/grupos/excluir_grupo.html', {'grupo': grupo})
