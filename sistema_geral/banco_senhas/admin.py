from django.contrib import admin
from django.db.models import Q
from .models import Categoria, Senha
from django.contrib.auth.models import User  # Importando User, caso esteja usando o modelo padrão

# Filtro personalizado para o usuário
class UsuarioFilter(admin.SimpleListFilter):
    title = 'usuário'  # O título do filtro
    parameter_name = 'usuario'  # O nome do parâmetro na URL

    def lookups(self, request, model_admin):
        # Retorna os usuários para que possam ser selecionados no filtro
        users = set(Categoria.objects.values_list('usuario', flat=True))
        # Exibir o nome do usuário 
        return [(user.id, str(user)) for user in User.objects.filter(id__in=users)]  # Exibindo nome completo

    def queryset(self, request, queryset):
        # Filtra as categorias que pertencem ao usuário selecionado
        if self.value():
            return queryset.filter(usuario_id=self.value())  # Filtra com o id do usuário
        return queryset

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_coletiva', 'usuario')
    list_filter = ('is_coletiva', UsuarioFilter)  # Adicionando o filtro personalizado

@admin.register(Senha)
class SenhaAdmin(admin.ModelAdmin):
    list_display = ('descricao','user','senha', 'is_coletiva', 'usuario', 'categoria','link')
    list_filter = ('is_coletiva', 'categoria')
