from django.urls import path

# Importando views específicas
from ordem_servico.views.chamado import (
    criar_chamado, listar_chamados, visualizar_chamado, encerrar_chamado, reabrir_chamado,
    meus_chamados, chamados_abertos, chamados_encerrados
)

from ordem_servico.views.adm_chamado import (
    adm_listar_chamados, adm_visualizar_chamado, atualizar_status,
    relatorio_chamados, gerar_relatorio_pdf, adm_meus_chamados, adm_chamados_abertos,
    adm_chamados_encerrados
)

from ordem_servico.views.contato import (
    criar_contato, listar_contatos, editar_contato, visualizar_contato, excluir_contato
)

from ordem_servico.views.mensagem import (
    enviar_mensagem, adm_enviar_mensagem
)

urlpatterns = [
    # Chamados
    path('criar/', criar_chamado, name='criar_chamado'),
    path('listar/', listar_chamados, name='listar_chamados'),
    path('visualizar/<int:id>/', visualizar_chamado, name='visualizar_chamado'),
    path('encerrar/<int:id>/', encerrar_chamado, name='encerrar_chamado'),
    path('reabrir/<int:pk>/', reabrir_chamado, name='reabrir_chamado'),
    path('mensagem/<int:id>/enviar/', enviar_mensagem, name='enviar_mensagem'),
    path('meus_chamados/', meus_chamados, name='meus_chamados'),# Menu Lateral para chamados
    path('chamados_abertos/', chamados_abertos, name='chamados_abertos'), # Menu Lateral para chamados
    path('chamados_encerrados/', chamados_encerrados, name='chamados_encerrados'),# Menu Lateral para chamados

    # Chamados Administrador
    path('admlistar/', adm_listar_chamados, name='adm_listar_chamados'),
    path('admvisualizar/<int:id>/', adm_visualizar_chamado, name='adm_visualizar_chamado'),
    path('admvisualizar/<int:chamado_id>/atualizar-status/', atualizar_status, name='atualizar_status'),
    path('admmensagem/<int:id>/enviar/', adm_enviar_mensagem, name='adm_enviar_mensagem'),
    path('relatorio-chamados/', relatorio_chamados, name='relatorio_chamados'),
    path('relatorio/chamados/pdf/', gerar_relatorio_pdf, name='os_gerar_relatorio_pdf'),

    path('admmeus_chamados/', adm_meus_chamados, name='adm_meus_chamados'),    # Menu Lateral para chamados administrador
    path('admchamados_abertos/', adm_chamados_abertos, name='adm_chamados_abertos'),    # Menu Lateral para chamados administrador
    path('admchamados_encerrados/', adm_chamados_encerrados, name='adm_chamados_encerrados'),    # Menu Lateral para chamados administrador

    # Contatos
    path('criar_contato/', criar_contato, name='criar_contato'),
    path('listar_contato/', listar_contatos, name='listar_contatos'),
    path('editar_contato/<int:id>/', editar_contato, name='editar_contato'),
    path('visualizar_contato/<int:id>/', visualizar_contato, name='visualizar_contato'),
    path('excluir_contato/<int:id>/', excluir_contato, name='excluir_contato'),
]
