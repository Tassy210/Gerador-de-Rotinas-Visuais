from django import forms
from .models import Atividade

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao', 'pictograma', 'ordem']