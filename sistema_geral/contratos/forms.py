# seu_app/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Contrato
from decimal import Decimal
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile # Importe esta classe

class ContratoForm(forms.ModelForm):
    usuario_responsavel = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-required': 'true',
        }),
        label="Usuário Responsável",
        empty_label="Selecione um usuário",
    )

    class Meta:
        model = Contrato
        fields = [
            'documento', 'razao_social', 'nome_fantasia', 'telefone',
            'email', 'descricao', 'data_assinatura', 'data_validade',
            'valor', 'usuario_responsavel', 'arquivo_contrato',
        ]

        widgets = {
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o documento (somente números)',
                'required': True,
                'aria-required': 'true',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',
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
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o telefone (somente números)',
            }),
            'email': forms.EmailInput(attrs={
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
            'valor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'R$ ',
                'required': False,
                'aria-required': 'false',
            }),
            'arquivo_contrato': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            return Decimal('0.00')
        if isinstance(valor, Decimal):
            return valor
        if isinstance(valor, str):
            valor_limpo = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
            try:
                valor_decimal = Decimal(valor_limpo)
            except Exception:
                raise forms.ValidationError("Por favor, insira um valor numérico válido (ex: 1500.00 ou 1500,00).")
            return valor_decimal
        raise forms.ValidationError("Valor inválido.")

    def clean_arquivo_contrato(self):
        arquivo = self.cleaned_data.get('arquivo_contrato')

        # A validação de tamanho e tipo deve ocorrer SOMENTE se um NOVO arquivo foi enviado.
        # Se 'arquivo' for None (nenhum arquivo selecionado) ou uma instância de FieldFile
        # (arquivo existente que não foi alterado), não precisamos validar content_type ou size.
        if isinstance(arquivo, UploadedFile): # Verifica se é um arquivo recém-enviado
            if arquivo.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError(
                    f"O arquivo excede o tamanho máximo permitido de {settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024):.0f} MB."
                )

            allowed_content_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'image/jpeg',
                'image/png',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            ]
            if arquivo.content_type not in allowed_content_types:
                raise forms.ValidationError("Tipo de arquivo não permitido. Por favor, faça upload de PDF, DOCX, JPG, PNG ou Excel.")
        
        return arquivo

    def clean_documento(self):
        documento = self.cleaned_data['documento']
        documento = ''.join(filter(str.isdigit, documento))
        if len(documento) not in [11, 14]:
            raise forms.ValidationError("Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos.")
        return documento

    def clean_razao_social(self):
        return self.cleaned_data['razao_social'].upper()

    def clean_nome_fantasia(self):
        return self.cleaned_data['nome_fantasia'].upper()

    def clean_descricao(self):
        return self.cleaned_data['descricao'].upper()

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if telefone:
            telefone = ''.join(filter(str.isdigit, str(telefone)))
        return telefone
