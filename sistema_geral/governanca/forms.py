from decimal import Decimal
from django import forms
from governanca.models import ItemLavanderia, Funcionarios, ControleQuartos, MotivoAusencia
from .models import RelatorioLav

class ItemLavanderiaForm(forms.ModelForm):
    class Meta:
        model = ItemLavanderia
        fields = ['nome', 'pesokg', 'valormedio']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome',
                'required': 'required',
                'id': 'nome'
            }),
            'pesokg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2.50',
                'required': 'required',
                'id': 'pesokg'
            }),
            'valormedio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 10.00',
                'required': 'required',
                'id': 'valormedio'
            })
        }


class RelatorioLavForm(forms.ModelForm):
    class Meta:
        model = RelatorioLav
        fields = ['vrTotal', 'pesoTotal']

# ======= FORMS PARA SISTEMA DE QUARTOS =======

class FuncionariosForm(forms.ModelForm):
    class Meta:
        model = Funcionarios
        fields = ['nome', 'cargo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
                'required': 'required',
                'id': 'nome'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Camareira, Supervisor...',
                'required': 'required',
                'id': 'cargo'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'ativo'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome Completo'
        self.fields['cargo'].label = 'Cargo'
        self.fields['ativo'].label = 'Funcionário Ativo'


class ControleQuartosForm(forms.ModelForm):
    class Meta:
        model = ControleQuartos
        fields = [
            'data', 'funcionario', 'motivo_ausencia', 'permanece_entrada', 'saida_entrada', 
            'quantidade_quartos', 'reservas_realizadas', 'permanece_realizadas', 
            'saidas_realizadas'
        ]
        widgets = {
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required',
                'id': 'data'
            }),
            'funcionario': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required',
                'id': 'funcionario'
            }),
            'motivo_ausencia': forms.Select(attrs={
                'class': 'form-select',
                'id': 'motivo_ausencia'
            }),
            'permanece_entrada': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Meta de quartos permanece',
                'id': 'permanece_entrada'
            }),
            'saida_entrada': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Meta de quartos de saída',
                'id': 'saida_entrada'
            }),
            'quantidade_quartos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ex: 16 (padrão)',
                'required': 'required',
                'id': 'quantidade_quartos'
            }),
            'reservas_realizadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Reservas (quartos de saída do tipo reserva)',
                'id': 'reservas_realizadas'
            }),
            'permanece_realizadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Permanece realizado',
                'id': 'permanece_realizadas'
            }),
            'saidas_realizadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Saídas realizadas',
                'id': 'saidas_realizadas'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Labels customizados
        self.fields['data'].label = 'Data'
        self.fields['funcionario'].label = 'Funcionário'
        self.fields['motivo_ausencia'].label = 'Motivo de Ausência (Opcional)'
        self.fields['permanece_entrada'].label = 'Meta Permanece (Entradas)'
        self.fields['saida_entrada'].label = 'Meta Saídas'
        self.fields['quantidade_quartos'].label = 'Total de Quartos do Dia'
        self.fields['reservas_realizadas'].label = 'Reservas Realizadas (Quartos de Saída)'
        self.fields['permanece_realizadas'].label = 'Permanece Realizadas'
        self.fields['saidas_realizadas'].label = 'Saídas Realizadas'
        
        # Configurar motivo de ausência
        self.fields['motivo_ausencia'].queryset = MotivoAusencia.objects.filter(ativo=True).order_by('nome')
        self.fields['motivo_ausencia'].empty_label = "-- Trabalho Normal --"
        self.fields['motivo_ausencia'].help_text = "Se preenchido, os valores de metas e realizações serão zerados automaticamente"
        
        # Define valor padrão para Quartos do Dia (apenas para novos registros)
        if not self.instance.pk:  # Apenas para criação, não para edição
            self.fields['quantidade_quartos'].initial = 16

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        funcionario = cleaned_data.get('funcionario')
        
        if data and funcionario:
            # Verifica se já existe um registro para esta data e funcionário
            if self.instance.pk:  # Se estamos editando
                exists = ControleQuartos.objects.filter(
                    data=data, funcionario=funcionario
                ).exclude(pk=self.instance.pk).exists()
            else:  # Se estamos criando
                exists = ControleQuartos.objects.filter(
                    data=data, funcionario=funcionario
                ).exists()
                
            if exists:
                raise forms.ValidationError(
                    f'Já existe um registro para {funcionario.nome} na data {data.strftime("%d/%m/%Y")}.',
                    code='registro_existente'
                )
        
        return cleaned_data


class FiltroControleQuartosForm(forms.Form):
    """Form para filtros de listagem"""
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'data_inicio'
        }),
        label='Data Início'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'data_fim'
        }),
        label='Data Fim'
    )
    
    funcionario = forms.ModelChoiceField(
        queryset=Funcionarios.objects.filter(ativo=True).order_by('nome'),
        required=False,
        empty_label="Todos os funcionários",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'funcionario'
        }),
        label='Funcionário'
    )


class MotivoAusenciaForm(forms.ModelForm):
    """Form para cadastro e edição de motivos de ausência"""
    
    class Meta:
        model = MotivoAusencia
        fields = ['nome', 'descricao', 'cor', 'afeta_media', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Férias, Atestado, Folga...',
                'required': 'required',
                'id': 'nome'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição detalhada do motivo (opcional)',
                'id': 'descricao'
            }),
            'cor': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'id': 'cor'
            }),
            'afeta_media': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'afeta_media'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'ativo'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Labels customizados
        self.fields['nome'].label = 'Nome do Motivo'
        self.fields['descricao'].label = 'Descrição'
        self.fields['cor'].label = 'Cor de Identificação'
        self.fields['afeta_media'].label = 'Afeta Média de Performance'
        self.fields['ativo'].label = 'Motivo Ativo'
        
        # Help texts
        self.fields['cor'].help_text = 'Cor utilizada para destacar este motivo nos relatórios'
        self.fields['afeta_media'].help_text = 'Marque se este motivo deve impactar negativamente nas estatísticas (ex: falta não justificada)'
        self.fields['ativo'].help_text = 'Desmarque para desativar este motivo (não aparecerá nas listas)'
        
        # Bloquear edição para motivos do sistema
        if self.instance.pk and self.instance.sistema:
            for field_name in ['nome', 'afeta_media']:
                self.fields[field_name].widget.attrs['readonly'] = True
                self.fields[field_name].disabled = True
            
            # Adicionar aviso visual
            self.fields['nome'].help_text = '🔒 Este é um motivo do sistema e não pode ser editado'
            self.fields['afeta_media'].help_text = '🔒 Este campo não pode ser alterado para motivos do sistema'

    def clean(self):
        cleaned_data = super().clean()
        
        # Validação extra para motivos do sistema
        if self.instance.pk and self.instance.sistema:
            # Não permitir mudança do nome
            if cleaned_data.get('nome') != self.instance.nome:
                raise forms.ValidationError('O nome de motivos do sistema não pode ser alterado.')
            
            # Não permitir mudança do campo afeta_media
            if cleaned_data.get('afeta_media') != self.instance.afeta_media:
                raise forms.ValidationError('O campo "Afeta Média" não pode ser alterado para motivos do sistema.')
        
        return cleaned_data
