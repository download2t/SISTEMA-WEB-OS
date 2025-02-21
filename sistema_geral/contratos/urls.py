from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_contratos, name='listar_contratos'),
    path('criar/', views.criar_contrato, name='criar_contrato'),
    path('editar/<int:contrato_id>/', views.editar_contrato, name='editar_contrato'),
    path('inativar/<int:contrato_id>/', views.inativar_contrato, name='inativar_contrato'),
    path('ativar/<int:contrato_id>/', views.ativar_contrato, name='ativar_contrato'),
    path('vencendo/', views.contratos_vencendo, name='contratos_vencendo'),
    path('relatorio/', views.listar_contratos_rel, name='listar_contratos_rel'),
    path('relatorio/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('relatorio/word/', views.generate_word, name='generate_word'),
    path('relatorio/excel/', views.generate_excel, name='generate_excel'),
]