from django import forms
from .models import Rotina, Categoria, Atividade
from django.contrib.auth.models import User

class RotinaForm(forms.ModelForm):
    class Meta:
        model = Rotina

        fields = ['titulo', 'descricao', 'categoria'] 
        
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-none rounded-t-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Título da Rotina (Ex: Rotina da Manhã)',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'relative block w-full appearance-none rounded-none border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Descreva os passos ou o objetivo desta rotina.',
                'rows': 3,
            }),

            'categoria': forms.Select(attrs={

                'class': 'relative block w-full appearance-none rounded-none border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
            }),

            'pictograma_upload': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 relative block w-full appearance-none rounded-none rounded-b-md border border-slate-300 px-3 py-2',
            }),            

        }

pass

class CategoriaForm(forms.ModelForm): 
    class Meta: 
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
                'placeholder': 'Nome da nova categoria (Ex: Lazer)',
                'required': True
           })
        }
        
class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade 
        
        fields = ['titulo', 'descricao', 'pictograma']
        
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-none rounded-t-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Título da Atividade (Ex: Escovar os dentes)',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'relative block w-full appearance-none rounded-none border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Descreva esta etapa (opcional)',
                'rows': 3,
            }),
            'pictograma': forms.FileInput(attrs={

                'class': 'block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 relative block w-full appearance-none rounded-none rounded-b-md border border-slate-300 px-3 py-2',
            }),
            
        }