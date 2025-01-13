from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf.urls import handler403
from django.conf import settings
from django.conf.urls.static import static

# Função personalizada para o erro 403
def custom_permission_denied_view(request, exception=None):
    return render(request, 'core/403.html', status=403)

# Definindo o handler do erro 403
handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls),           # Painel de administração
    path('', include('core.urls')),           # Rotas do app core
    path('ordem-servico/', include('ordem_servico.urls')),  # Rotas do app ordem_servico
    path('ramais/', include('ramais.urls')),  # Rotas do app stores
    path('banco-senhas/', include('banco_senhas.urls')),  # Rotas do app banco_senhas
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
