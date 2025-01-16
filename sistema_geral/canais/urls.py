from django.urls import path
from . import views

urlpatterns = [
    #Canais
    path('canais/', views.listar_canais, name='listar_canais'),
    path('criar_canal/', views.criar_canal, name='criar_canal'),  # Exemplo de URL para criação
    path('editar_canal/<int:canal_id>/', views.editar_canal, name='editar_canal'),
    path('excluir_canal/<int:canal_id>/', views.excluir_canal, name='excluir_canal'),  # Exemplo de URL para exclusão

    #Listas
    path('listar_listas/', views.listar_listas, name='listar_listas'),
    path('criar_lista/', views.criar_lista, name='criar_lista'),
    path('editar_lista/<int:lista_id>/', views.editar_lista, name='editar_lista'),
    path('excluir_lista/<int:lista_id>/', views.excluir_lista, name='excluir_lista'),
    path('canais_tv/', views.ultima_lista, name='canais_tv'),  # Pg inicial mostrando a lista + atual

    path('listas/download/', views.download_pdf, name='download_pdf'),
    path('download/', views.download_pdf_canais, name='download_pdf_canais'),
]
