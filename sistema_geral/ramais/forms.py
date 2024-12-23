from django import forms
from .models import Ramal
from django.contrib.auth.models import Group

class RamalForm(forms.ModelForm):
    class Meta:
        model = Ramal
        fields = ['numero_ramal', 'atendente', 'linha_completa', 'grupo', 'ativo']

    def clean_numero_ramal(self):
        numero_ramal = self.cleaned_data['numero_ramal']
        ramal = self.instance  # O ramal que está sendo editado

        # Verifica se o número do ramal foi alterado. Se não foi, não precisa validar a unicidade.
        if ramal.pk and ramal.numero_ramal != numero_ramal:  # Verifica se é uma edição
            if Ramal.objects.filter(numero_ramal=numero_ramal).exists():
                raise forms.ValidationError("Ramal com este número já existe.")
        
        return numero_ramal
