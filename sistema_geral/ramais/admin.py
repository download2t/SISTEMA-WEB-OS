# admin.py
from django.contrib import admin
from .models import Ramal

@admin.register(Ramal)
class RamalAdmin(admin.ModelAdmin):
    list_display = ('numero_ramal', 'linha_completa', 'grupo', 'atendente')
    search_fields = ('numero_ramal', 'linha_completa', 'atendente')
    list_filter = ('grupo',)
    ordering = ('numero_ramal',)
