from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'relative block w-full appearance-none rounded-none rounded-t-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
            'placeholder': 'Nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'relative block w-full appearance-none rounded-none border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'relative block w-full appearance-none rounded-none rounded-b-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
            'placeholder': 'Confirme a senha'
        })

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'relative block w-full appearance-none rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm',
                'placeholder': 'E-mail'
            }),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }