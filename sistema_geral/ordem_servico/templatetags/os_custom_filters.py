from hashlib import md5
from django import template

register = template.Library()

@register.filter
def file_extension(file_name, extensions):
    """
    Verifica se o arquivo possui uma das extensões especificadas.
    Uso no template: {{ file_name|file_extension:"jpg,png,pdf" }}
    """
    return file_name.lower().endswith(tuple(extensions.split(',')))

# Lista de cores disponíveis
CORES = [

    "#007bff",  # Azul
    "#28a745",  # Verde
    "#6c757d",  # Cinza
    "#ff5733",  # Laranja (Exemplo de nova cor)
    "#8e44ad",  # Roxo (Exemplo de nova cor)
    #"#dc3545",  # Vermelho

]

@register.filter
def cor_usuario(usuario):
    """
    Gera uma cor fixa para cada usuário baseado no hash do nome.
    """
    index = int(md5(usuario.username.encode()).hexdigest(), 16) % len(CORES)
    return CORES[index]

