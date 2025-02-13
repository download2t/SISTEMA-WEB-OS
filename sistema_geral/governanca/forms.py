from decimal import Decimal
from django import forms
from governanca.models import ItemLavanderia
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
