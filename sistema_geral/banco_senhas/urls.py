# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs para Senhas
    path('senhas/selecionar', views.selecionar, name='selecionar'),
    path('senhas/', views.listar_senhas, name='listar_senhas'),
    path('senhas/adicionar_privado/', views.adicionar_senha_privada, name='adicionar_senha_privada'),
    path('senhas/adicionar_publica/', views.adicionar_senha_publica, name='adicionar_senha_publica'),
    path('senhas/editar_privado/<int:senha_id>/', views.editar_senha_privada, name='editar_senha_privada'),
    path('senhas/editar_publica/<int:senha_id>/', views.editar_senha_publica, name='editar_senha_publica'),
    path('senhas/visualizar/<int:senha_id>/', views.visualizar_senha, name='visualizar_senha'),


    path('senhas/excluir/<int:pk>/', views.excluir_senha, name='excluir_senha'),
    
    # URLs para Categorias
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/adicionar/', views.adicionar_categoria, name='adicionar_categoria'),
    path('categorias/adicionar_pop_priv/', views.adicionar_categoria_senhas_privado, name='adicionar_categoria_senhas_privado'),
    path('categorias/adicionar_pop_pub/', views.adicionar_categoria_senhas_publico, name='adicionar_categoria_senhas_publico'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/excluir/<int:pk>/', views.excluir_categoria, name='excluir_categoria'),
    path('categorias/<str:tipo_banco>/', views.listar_categorias, name='listar_categorias'),
]
 