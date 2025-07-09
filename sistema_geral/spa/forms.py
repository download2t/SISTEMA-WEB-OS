# spa/forms.py
from django import forms
from .models import Agendamento, TipoMassagem
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'nome_hospede', 'telefone', 'email',
            'numero_quarto', 'numero_reserva',
            'data', 'horario','tipo_massagem',
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
        }
        help_texts = {
            'numero_quarto': 'Opcional',
            'numero_reserva': 'Opcional',
            'primeira_vez': 'Marque se for a primeira vez do hóspede no spa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_massagem'].queryset = TipoMassagem.objects.filter(ativo=True)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')
        tipo_massagem = cleaned_data.get('tipo_massagem')

        errors = {}

        if tipo_massagem and not tipo_massagem.ativo:
            errors['tipo_massagem'] = 'Este tipo de massagem não está disponível no momento.'

        if data and horario: # Remove 'and not self.instance.pk' if you want to apply this validation to edits too
            # Combine date and time to a naive datetime object
            agendamento_naive_datetime = datetime.combine(data, horario)
            
            # Make the naive datetime aware using the current timezone (settings.TIME_ZONE)
            # This is the crucial change
            agendamento_aware_datetime = timezone.make_aware(agendamento_naive_datetime, timezone.get_current_timezone())

            # Now compare aware with aware
            if agendamento_aware_datetime < timezone.now():
                # Compare only dates if the entire datetime is in the past
                if data < timezone.now().date():
                    errors['data'] = "Não é possível agendar para datas passadas."
                # If it's today, check if the time is in the past
                elif data == timezone.now().date() and horario < timezone.now().time():
                    errors['horario'] = "Não é possível agendar para horários passados no dia de hoje."
        
        # Original validation logic for conflicts (ensure it also handles timezone correctly if querying datetimes)
        # For querying `data` (DateField) and `horario` (TimeField) separately, timezone awareness is less critical
        # but if you were to query a DateTimeField, ensure consistency.
        if data and horario and not self.instance.pk: # Apply conflict check only for new appointments
            qs = Agendamento.objects.filter(
                data=data,
                horario=horario,
                status__in=['agendado', 'confirmado', 'em_andamento']
            )
            if qs.exists():
                errors['__all__'] = 'Já existe um agendamento para este horário.'


        if errors:
            raise ValidationError(errors)
            
        return cleaned_data
    

class EdicaoAgendamentoForm(forms.ModelForm):
    # O campo motivo_cancelamento pode permanecer, pois é útil se o status for 'cancelado'
    motivo_cancelamento = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Informe o motivo do cancelamento (se aplicável)...'
        }),
        label="Motivo do Cancelamento"
    )

    class Meta:
        model = Agendamento
        fields = [
            'nome_hospede', 'telefone', 'email',
            'numero_quarto', 'numero_reserva',
            'data', 'horario', 'tipo_massagem',
            'primeira_vez', 'observacoes', 'status'
        ]
        widgets = {
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
                format='%Y-%m-%d'
            ),
             'horario': forms.TimeInput( # Added missing widget for 'horario' in EdicaoAgendamentoForm
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
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
        self.fields['tipo_massagem'].queryset = TipoMassagem.objects.filter(ativo=True)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        motivo = cleaned_data.get('motivo_cancelamento')
    
        tipo_massagem = cleaned_data.get('tipo_massagem')

        errors = {}

        if tipo_massagem and not tipo_massagem.ativo:
            errors['tipo_massagem'] = 'Este tipo de massagem não está disponível no momento.'
        
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')

        # Add similar timezone-aware validation for EdicaoAgendamentoForm if needed
        # (This depends on whether you want to prevent editing an appointment to a past time/date)
        if data and horario:
            agendamento_naive_datetime = datetime.combine(data, horario)
            agendamento_aware_datetime = timezone.make_aware(agendamento_naive_datetime, timezone.get_current_timezone())

            if agendamento_aware_datetime < timezone.now():
                pass # Or add specific validation based on your editing rules


        if data and horario:
            qs = Agendamento.objects.filter(
                data=data,
                horario=horario,
                status__in=['agendado', 'confirmado', 'em_andamento']
            )
            if self.instance.pk: # If it's an existing instance (editing)
                qs = qs.exclude(pk=self.instance.pk) # Exclude the current object from the check

            if qs.exists():
                errors['__all__'] = 'Já existe outro agendamento para este horário.'


        if errors:
            raise ValidationError(errors)

        return cleaned_data
    
class TipoMassagemForm(forms.ModelForm):
    class Meta:
        model = TipoMassagem
        fields = ['nome', 'descricao', 'duracao_minutos', 'preco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da massagem'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descrição da massagem'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'step': 15}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'nome': 'Nome da Massagem',
            'descricao': 'Descrição',
            'duracao_minutos': 'Duração (minutos)',
            'preco': 'Preço (R$)',
            'ativo': 'Disponível para agendamento?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica a classe form-control para todos os campos não-checkbox
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-control')
            else:
                field.widget.attrs.setdefault('class', 'form-check-input')