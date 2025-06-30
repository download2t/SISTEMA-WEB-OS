from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_spa, name='listar_spa'),
    path('novo/', views.cadastro_spa, name='cadastro_spa'),
    path('editar/<int:pk>/', views.editar_spa, name='editar_spa'),
    path('cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_spa'),
    path('confirmar/<int:pk>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('iniciar/<int:pk>/', views.iniciar_servico, name='iniciar_servico'),
    path('finalizar/<int:pk>/', views.finalizar_servico, name='finalizar_servico'),
    path('nao-compareceu/<int:pk>/', views.nao_compareceu, name='nao_compareceu'),
    path('reativar/<int:pk>/', views.reativar_agendamento, name='reativar_agendamento'),
]