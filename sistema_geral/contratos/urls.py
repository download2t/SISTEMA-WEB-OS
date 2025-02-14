from django.urls import path
from . import views

urlpatterns = [
    path('contratos/', views.listar_contratos, name='listar_contratos'),
    path('contratos/criar/', views.criar_contrato, name='criar_contrato'),
    path('contratos/editar/<int:contrato_id>/', views.editar_contrato, name='editar_contrato'),
    path('contratos/inativar/<int:contrato_id>/', views.inativar_contrato, name='inativar_contrato'),
    path('contratos/ativar/<int:contrato_id>/', views.ativar_contrato, name='ativar_contrato'),
]
