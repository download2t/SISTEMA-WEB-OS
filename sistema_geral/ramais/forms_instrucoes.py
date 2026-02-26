from django import forms

class InstrucoesPDFForm(forms.Form):
    instrucoes = forms.CharField(
        label="Instruções para rodapé do PDF",
        widget=forms.Textarea(attrs={"rows": 5, "class": "form-control", "placeholder": "Digite as instruções do rodapé do PDF..."}),
        required=False,
    )
