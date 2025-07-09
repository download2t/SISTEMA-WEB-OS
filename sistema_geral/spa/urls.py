# spa/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... (Seus URLs existentes para Agendamento) ...

    # URLs de Agendamento
    path('', views.listar_spa, name='listar_spa'),
    path('agendados-hoje/', views.listar_spa, {'filter_type': 'hoje'}, name='agendados_hoje'),
    path('cancelados/', views.listar_spa, {'filter_type': 'cancelados'}, name='cancelados_spa'),
    path('realizados/', views.listar_spa, {'filter_type': 'realizados'}, name='encerrados_spa'),
    
    path('novo/', views.cadastro_spa, name='cadastro_spa'),
    path('editar/<int:pk>/', views.editar_spa, name='editar_spa'),
    path('cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_spa'),
    path('confirmar/<int:pk>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('iniciar/<int:pk>/', views.iniciar_servico, name='iniciar_servico'),
    path('finalizar/<int:pk>/', views.finalizar_servico, name='finalizar_servico'),
    path('nao-compareceu/<int:pk>/', views.nao_compareceu, name='nao_compareceu'),
    path('reativar/<int:pk>/', views.reativar_agendamento, name='reativar_agendamento'),
    
    # URL para Relatórios
    path('relatorios/', views.relatorio_spa, name='relatorio_spa'),

    # URLs para TipoMassagem
    path('massagens/', views.listar_massagens, name='listar_massagens'),
    path('massagens/nova/', views.criar_massagem, name='criar_massagem'),
    path('massagens/editar/<int:pk>/', views.editar_massagem, name='editar_massagem'),
    path('massagens/inativar/<int:pk>/', views.inativar_massagem, name='inativar_massagem'),
    path('massagens/visualizar/<int:pk>/', views.visualizar_massagem, name='visualizar_massagem'),
    # NOVO: URL para reativar massagem
    path('massagens/reativar/<int:pk>/', views.reativar_massagem, name='reativar_massagem'),
]