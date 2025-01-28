from django import forms
from .models import ListaCanais, Canal

class CanalForm(forms.ModelForm):
    class Meta:
        model = Canal
        fields = ['numero', 'titulo', 'status']  # Adicionado o campo 'status'
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o número do canal',
                'required': 'required',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do canal',
                'required': 'required',
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'numero': 'Número do Canal',
            'titulo': 'Título do Canal',
            'status': 'Ativo',  # Rotulo para o campo status
        }

class ListaCanaisForm(forms.ModelForm):
    class Meta:
        model = ListaCanais
        fields = ['data_criacao', 'canais']

    data_criacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data de Criação'
    )
