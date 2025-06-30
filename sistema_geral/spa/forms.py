from django import forms
from .models import Agendamento, TipoMassagem
from django.core.exceptions import ValidationError
from django.utils import timezone


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'nome_hospede', 'telefone', 'email', 
            'numero_quarto', 'numero_reserva',
            'data', 'horario', 'duracao', 'tipo_massagem',
            'primeira_vez', 'observacoes'
        ]
        widgets = {
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': timezone.now().date().isoformat()
                },
                format='%Y-%m-%d'
            ),
            'horario': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                },
                format='%H:%M'
            ),
            'observacoes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Informe alergias, preferências de pressão, áreas específicas para trabalhar...'
                }
            ),
            'tipo_massagem': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'duracao': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 15,
                    'step': 15
                }
            )
        }
        help_texts = {
            'numero_quarto': 'Opcional',
            'numero_reserva': 'Opcional',
            'primeira_vez': 'Marque se for a primeira vez do hóspede no spa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas massagens ativas
        self.fields['tipo_massagem'].queryset = TipoMassagem.objects.filter(ativo=True)
        
        # Adiciona classes CSS a todos os campos
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
        
        # Configura o campo de duração se não estiver definido
        if not self.instance.pk and 'duracao' not in self.data:
            self.initial['duracao'] = 60  # Valor padrão

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data < timezone.now().date():
            raise ValidationError("Não é possível agendar para datas passadas.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')
        tipo_massagem = cleaned_data.get('tipo_massagem')
        
        # Verifica se o tipo de massagem está ativo
        if tipo_massagem and not tipo_massagem.ativo:
            raise ValidationError("Este tipo de massagem não está disponível no momento.")
        
        # Verifica conflitos de horário (opcional)
        if data and horario:
            # Implemente aqui a lógica para verificar conflitos de horário se necessário
            pass
            
        return cleaned_data
    


class EdicaoAgendamentoForm(forms.ModelForm):
    motivo_cancelamento = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Informe o motivo do cancelamento...'
        }),
        label="Motivo do Cancelamento"
    )

    class Meta:
        model = Agendamento
        fields = [
            'nome_hospede', 'telefone', 'email',
            'numero_quarto', 'numero_reserva',
            'data', 'horario', 'duracao', 'tipo_massagem',
            'primeira_vez', 'observacoes', 'status'
        ]
        widgets = {
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': timezone.now().date().isoformat()
                },
                format='%Y-%m-%d'
            ),
            'horario': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                },
                format='%H:%M'
            ),
            'observacoes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Informe alergias, preferências de pressão...'
                }
            ),
            'tipo_massagem': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'duracao': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 15,
                    'step': 15
                }
            )
        }

        def clean(self):
            cleaned_data = super().clean()
            status = cleaned_data.get('status')
            motivo = cleaned_data.get('motivo_cancelamento')
            data = cleaned_data.get('data')
            horario = cleaned_data.get('horario')
            tipo_massagem = cleaned_data.get('tipo_massagem')

            # Validações específicas
            errors = {}

            # 1. Validação para cancelamento
            if status == 'cancelado' and not motivo:
                errors['motivo_cancelamento'] = 'Informe o motivo do cancelamento'

            # 2. Validação de data/horário
            if data and data < timezone.now().date():
                errors['data'] = 'Não é possível agendar para datas passadas'
            
            if data and horario:
                if data == timezone.now().date() and horario < timezone.now().time():
                    errors['horario'] = 'Não é possível agendar para horários passados'

            # 3. Validação de tipo de massagem
            if tipo_massagem and not tipo_massagem.ativo:
                errors['tipo_massagem'] = 'Este tipo de massagem não está disponível'

            # 4. Validação de conflitos de horário (exemplo)
            if data and horario and not self.instance.pk:
                conflito = Agendamento.objects.filter(
                    data=data,
                    horario=horario,
                    status__in=['agendado', 'confirmado']
                ).exists()
                if conflito:
                    errors['__all__'] = 'Já existe um agendamento para este horário'

            if errors:
                raise ValidationError(errors)

            return cleaned_data