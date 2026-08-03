from django import forms
from .models import QueryRelatorio


class QueryRelatorioForm(forms.ModelForm):
    class Meta:
        model = QueryRelatorio
        # Aqui dizemos quais campos o usuário comum pode preencher
        fields = ['nome', 'descricao', 'codigo_sql','grupos_permitidos']

        # Opcional: Adicionando classes CSS para deixar mais bonito depois
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'codigo_sql': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'grupos_permitidos': forms.SelectMultiple(attrs={'class': 'form-control'})
        }