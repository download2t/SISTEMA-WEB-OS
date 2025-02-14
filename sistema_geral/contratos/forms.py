from django import forms
from .models import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['documento', 'razao_social', 'nome_fantasia', 'telefone', 'email', 'descricao', 'data_assinatura', 'data_validade', 'valor']
        
        widgets = {
            'documento': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o documento', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
            'razao_social': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite a razão social', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o nome fantasia',
                'aria-required': 'false',
            }),
            'telefone': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o telefone', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o e-mail', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Descrição do contrato',
                'aria-required': 'false',
            }),
            'data_assinatura': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control', 
                'type': 'date', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
            'data_validade': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control', 
                'type': 'date', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o valor', 
                'required': True,  # Campo obrigatório
                'aria-required': 'true',
            }),
        }
