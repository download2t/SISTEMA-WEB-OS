from email.headerregistry import Group
from django import forms

from core import models
from .models import Chamado, Mensagem, Contato

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['texto', 'arquivo']

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome_responsavel', 'numero_telefone', 'grupo', 'usuario']  # Adiciona 'usuario' aos campos
        widgets = {
            'nome_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),  # Adiciona um campo Select para o usuário
        }

