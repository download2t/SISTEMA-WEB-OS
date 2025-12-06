from django.urls import path
from .views.itens import create_item_lavanderia, update_item_lavanderia, delete_item_lavanderia, list_item_lavanderia,selecionarGov
from .views.relatorios import criar_relatorio, listar_relatorios,detalhar_relatorio,delete_relatorio
from .views.quartos import (
    # Funcionários
    listar_funcionarios, criar_funcionario, editar_funcionario, excluir_funcionario,
    # Controle de Quartos
    listar_controle_quartos, criar_controle_quartos, editar_controle_quartos, 
    excluir_controle_quartos, detalhar_controle_quartos, dashboard_quartos,
    # Motivos de Ausência
    listar_motivos_ausencia, criar_motivo_ausencia, editar_motivo_ausencia, excluir_motivo_ausencia,
    # API
    api_controle_quartos_data,
    # Relatórios
    relatorio_controle_quartos_pdf, relatorio_controle_quartos_excel, relatorio_controle_quartos_imprimir,
    # Gráfico PDF
    exportar_grafico_performance_pdf
)

urlpatterns = [
    # URLs de seleção
    path('governanca/governanca_index/', selecionarGov, name='selecionar_gov'),

    # URLs de itens da lavanderia
    path('lavanderia/novo/', create_item_lavanderia, name='create_item_lavanderia'),
    path('lavanderia/editar/<int:item_id>/', update_item_lavanderia, name='update_item_lavanderia'),
    path('lavanderia/excluir/<int:item_id>/', delete_item_lavanderia, name='delete_item_lavanderia'),
    path('lavanderia/list', list_item_lavanderia, name='item_lavanderia_list'),

    # URLs do relatório
    path('relatorio/criar/', criar_relatorio, name='criar_relatorio_lavanderia'),
    path('relatorio/excluir/<int:relatorio_id>/', delete_relatorio, name='excluir_relatorio'),
    path('relatorios/', listar_relatorios, name='listar_relatorios'),
    path('relatorio/<int:relatorio_id>/', detalhar_relatorio, name='detalhes_relatorio'),
    
    # ======= URLS PARA SISTEMA DE CONTROLE DE QUARTOS =======
    
    # Dashboard
    path('quartos/dashboard/', dashboard_quartos, name='dashboard_quartos'),
    
    # Funcionários
    path('quartos/funcionarios/', listar_funcionarios, name='listar_funcionarios'),
    path('quartos/funcionarios/criar/', criar_funcionario, name='criar_funcionario'),
    path('quartos/funcionarios/editar/<int:funcionario_id>/', editar_funcionario, name='editar_funcionario'),
    path('quartos/funcionarios/excluir/<int:funcionario_id>/', excluir_funcionario, name='excluir_funcionario'),
    
    # Controle de Quartos
    path('quartos/controle/', listar_controle_quartos, name='listar_controle_quartos'),
    path('quartos/controle/criar/', criar_controle_quartos, name='criar_controle_quartos'),
    path('quartos/controle/editar/<int:controle_id>/', editar_controle_quartos, name='editar_controle_quartos'),
    path('quartos/controle/excluir/<int:controle_id>/', excluir_controle_quartos, name='excluir_controle_quartos'),
    path('quartos/controle/detalhes/<int:controle_id>/', detalhar_controle_quartos, name='detalhar_controle_quartos'),
    
    # Motivos de Ausência
    path('quartos/motivos/', listar_motivos_ausencia, name='listar_motivos_ausencia'),
    path('quartos/motivos/criar/', criar_motivo_ausencia, name='criar_motivo_ausencia'),
    path('quartos/motivos/editar/<int:motivo_id>/', editar_motivo_ausencia, name='editar_motivo_ausencia'),
    path('quartos/motivos/excluir/<int:motivo_id>/', excluir_motivo_ausencia, name='excluir_motivo_ausencia'),
    
    # API
    path('api/quartos/data/', api_controle_quartos_data, name='api_controle_quartos_data'),
    
    # Relatórios
    path('quartos/relatorio/pdf/', relatorio_controle_quartos_pdf, name='relatorio_controle_quartos_pdf'),
    path('quartos/relatorio/excel/', relatorio_controle_quartos_excel, name='relatorio_controle_quartos_excel'),
    path('quartos/relatorio/imprimir/', relatorio_controle_quartos_imprimir, name='relatorio_controle_quartos_imprimir'),
    
    # Gráfico PDF
    path('quartos/grafico/pdf/', exportar_grafico_performance_pdf, name='exportar_grafico_performance_pdf'),
]
