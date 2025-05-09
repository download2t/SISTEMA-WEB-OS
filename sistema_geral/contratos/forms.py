from django import forms
from django.contrib.auth.models import Group
from .models import Contrato

class ContratoForm(forms.ModelForm):
    grupo_responsavel = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,  
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
                'placeholder': 'Digite o documento (somente números)', 
                'required': True,
                'aria-required': 'true',
                'maxlength': '14',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',  
            }),
            'razao_social': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite a razão social', 
                'required': True,
                'aria-required': 'true',
                'style': 'text-transform: uppercase;',
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o nome fantasia',
                'style': 'text-transform: uppercase;',
            }),
                'telefone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o telefone', 
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o e-mail', 
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Descrição do contrato',
                'style': 'text-transform: uppercase;',
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

    def clean_documento(self):
        documento = self.cleaned_data['documento']
        if not documento.isdigit():
            raise forms.ValidationError("O campo deve conter apenas números.")
        return documento

    def clean_razao_social(self):
        return self.cleaned_data['razao_social'].upper()

    def clean_nome_fantasia(self):
        return self.cleaned_data['nome_fantasia'].upper()

    def clean_descricao(self):
        return self.cleaned_data['descricao'].upper()
