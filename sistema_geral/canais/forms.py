from django import forms
from .models import ListaCanais, Canal
from django.db import models

class CanalForm(forms.ModelForm):
    class Meta:
        model = Canal
        fields = ['numero', 'titulo']
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
        }
        labels = {
            'numero': 'Número do Canal',
            'titulo': 'Título do Canal',
        }



class ListaCanaisForm(forms.ModelForm):
    class Meta:
        model = ListaCanais
        fields = ['data_criacao', 'canais']  # Inclua canais se você precisar deles também

    data_criacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Remova o readonly
        label='Data de Criação'
    )
