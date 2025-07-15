# contratos/templatetags/custom_filters.py

from django import template
import os

register = template.Library()

@register.filter
def filename(value):
    """
    Retorna apenas o nome do arquivo de um caminho completo.
    Funciona com:
    - FileField/ImageField (value.name)
    - String paths completos
    - URLs
    """
    if not value:
        return ""
    
    # Se for um objeto FileField/ImageField
    if hasattr(value, 'name'):
        path = value.name
    # Se já for uma string
    else:
        path = str(value)
    
    # Remove qualquer query string de URLs
    path = path.split('?')[0]
    # Remove qualquer fragmento de URL
    path = path.split('#')[0]
    
    # Extrai apenas o nome do arquivo
    return os.path.basename(path)