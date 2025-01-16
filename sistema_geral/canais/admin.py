from django.contrib import admin
from .models import Canal, ListaCanais

@admin.register(Canal)
class CanalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'titulo')

@admin.register(ListaCanais)
class ListaCanaisAdmin(admin.ModelAdmin):
    list_display = ('data_criacao',)
    filter_horizontal = ('canais',)
