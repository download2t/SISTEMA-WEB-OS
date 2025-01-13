from django import forms
from .models import Senha, Categoria

class SenhaFormPrivado(forms.ModelForm):
    user = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "form-control", 
        "placeholder": "Nome de usuário"
    }))  # Campo adicional para o "user"

    class Meta:
        model = Senha
        fields = ["categoria", "descricao", "user", "senha", "link", "is_coletiva"]
        widgets = {
            "descricao": forms.Textarea(attrs={
                "class": "form-control", 
                "placeholder": "Descrição da senha", 
                "rows": 3,  # Aumentei o número de linhas para 6
                "style": "resize: vertical;"  # Permite redimensionar verticalmente
            }),
            "user": forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário"}),
            "senha": forms.TextInput(attrs={"class": "form-control", "placeholder": "Senha"}),
            "link": forms.TextInput(attrs={"class": "form-control", "placeholder": "https://example.com"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "is_coletiva": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        senha = super().save(commit=False)
        senha.is_coletiva = False  # Garantir que é sempre "False"
        if commit:
            senha.save()
        return senha


class SenhaFormPublica(forms.ModelForm):
    user = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "form-control", 
        "placeholder": "Nome de usuário"
    }))  # Campo adicional para o "user"

    class Meta:
        model = Senha
        fields = ["categoria", "descricao", "user", "senha", "link", "is_coletiva"]
        widgets = {
                 "descricao": forms.Textarea(attrs={
                "class": "form-control", 
                "placeholder": "Descrição da senha", 
                "rows": 3,  # Aumentei o número de linhas para 6
                "style": "resize: vertical;"  # Permite redimensionar verticalmente
            }),
            "user": forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário"}),
            "senha": forms.TextInput(attrs={"class": "form-control", "placeholder": "Senha"}),
            "link": forms.TextInput(attrs={"class": "form-control", "placeholder": "https://example.com"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "is_coletiva": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        senha = super().save(commit=False)
        senha.is_coletiva = True  # Garantir que é sempre "True"
        if commit:
            senha.save()
        return senha

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'is_coletiva']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 3}),
            'is_coletiva': forms.RadioSelect(attrs={'class': 'form-control'}),  # Alterado para RadioSelect
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pegando o usuário logado
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.user = user  # Armazenando o usuário logado
        # Definindo o campo 'is_coletiva' com as opções "Privado" e "Coletivo"
        self.fields['is_coletiva'].choices = [
            (True, 'Coletivo'),
            (False, 'Privado'),
        ]

    def save(self, commit=True):
        categoria = super().save(commit=False)
        if not categoria.usuario:  # Caso o usuário não seja atribuído, atribui o usuário logado
            categoria.usuario = self.user  # Atribuindo o usuário logado
        
        if commit:
            categoria.save()
        return categoria
