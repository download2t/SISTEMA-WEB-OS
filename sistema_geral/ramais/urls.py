# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_ramais, name='listar_ramais'),
    path('adicionar/', views.adicionar_ramal, name='adicionar_ramal'),
    path('editar/<int:pk>/', views.editar_ramal, name='editar_ramal'),
    path('excluir/<int:pk>/', views.excluir_ramal, name='excluir_ramal'),
]