from django.urls import path
from . import views
from .views import alterar_senha, cadastrar_usuario, pesquisar_usuarios
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),
    path('accounts/profile/', views.home, name='home'),  # Redirecionamento após login
    
    # URLs de autenticação
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_confirm, name='logout_confirm'),  # Confirmação de logout
    path('logout/confirm/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout
    
    # Página de acesso negado
    path('nao_autenticado/', views.nao_autenticado, name='nao_autenticado'),
    path('403/', views.error_403_view, name='403'),
    
    ## ACCOUNTS
    path('accounts/alterar_senha/', alterar_senha, name='alterar_senha'),  # Alterar senha
    path('accounts/cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),  # Cadastrar usuário
    path('accounts/listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),  # Listar usuários
    path('accounts/<int:user_id>/ativar_usuario/', views.ativar_usuario_toggle, name='ativar_usuario'),
    path('accounts/<int:user_id>/desativar_usuario/', views.desativar_usuario_toggle, name='desativar_usuario'),
    path('accounts/alterar/<int:user_id>/', views.alterar_usuario, name='alterar_usuario'),  # Alterar dados do usuário
    
    ##Grupos
    path('grupos/listar_grupos', views.listar_grupos, name='listar_grupos'),
    path('grupos/criar_grupo', views.criar_grupo, name='criar_grupo'),
    path('grupos/editar/<int:grupo_id>/', views.editar_grupo, name='editar_grupo'),
    path('grupos/excluir/<int:grupo_id>/', views.excluir_grupo, name='excluir_grupo'),

]
