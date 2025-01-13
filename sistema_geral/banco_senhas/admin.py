from django.contrib import admin
from .models import Categoria, Senha

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_coletiva', 'usuario')
    list_filter = ('is_coletiva',)

@admin.register(Senha)
class SenhaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'is_coletiva', 'usuario', 'categoria')
    list_filter = ('is_coletiva', 'categoria')
