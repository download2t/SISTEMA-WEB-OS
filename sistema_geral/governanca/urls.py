from django.urls import path
from .views.itens import create_item_lavanderia, update_item_lavanderia, delete_item_lavanderia, list_item_lavanderia,selecionarGov
from .views.relatorios import criar_relatorio, listar_relatorios,detalhar_relatorio,delete_relatorio

urlpatterns = [
    # URLs  de seleçãow
    path('governanca/governanca_index/', selecionarGov, name='selecionar_gov'),

    # URLs de itens da lavanderia
    path('lavanderia/novo/', create_item_lavanderia, name='create_item_lavanderia'),
    path('lavanderia/editar/<int:item_id>/', update_item_lavanderia, name='update_item_lavanderia'),
    path('lavanderia/excluir/<int:item_id>/', delete_item_lavanderia, name='delete_item_lavanderia'),
    path('lavanderia/list', list_item_lavanderia, name='item_lavanderia_list'),

    # URLs do relatorio
    path('relatorio/criar/', criar_relatorio, name='criar_relatorio_lavanderia'),
    path('relatorio/excluir/<int:relatorio_id>/', delete_relatorio, name='excluir_relatorio'),
    path('relatorios/', listar_relatorios, name='listar_relatorios'),
    path('relatorio/<int:relatorio_id>/', detalhar_relatorio, name='detalhes_relatorio'),
    
]
