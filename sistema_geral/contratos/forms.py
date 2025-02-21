from django import forms
from django.contrib.auth.models import Group
from .models import Contrato

class ContratoForm(forms.ModelForm):
    grupo_responsavel = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,  # Campo obrigatório
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-required': 'true',
        }),
        label="Grupo Responsável"
    )

    class Meta:
        model = Contrato
        fields = [
            'documento', 'razao_social', 'nome_fantasia', 'telefone',  
            'email', 'descricao', 'data_assinatura', 'data_validade', 
            'valor', 'grupo_responsavel'
        ]

        widgets = {
            'documento': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o documento', 
                'required': True,
                'aria-required': 'true',
            }),
            'razao_social': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite a razão social', 
                'required': True,
                'aria-required': 'true',
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o nome fantasia',
            }),
            'telefone': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o telefone', 
                'required': True,
                'aria-required': 'true',
            }),
            'email': forms.EmailInput(attrs={  # Agora opcional
                'class': 'form-control', 
                'placeholder': 'Digite o e-mail', 
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Descrição do contrato',
            }),
            'data_assinatura': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control', 
                'type': 'date', 
                'required': True,
                'aria-required': 'true',
            }),
            'data_validade': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control', 
                'type': 'date', 
                'required': True,
                'aria-required': 'true',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o valor', 
                'required': True,
                'aria-required': 'true',
            }),
        }