from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login 
from .models import Atividade
from usuarios.forms import CustomUserCreationForm

@login_required
def home(request):
    atividades = Atividade.objects.filter(usuario=request.user).order_by('ordem')
    context = { 'atividades': atividades }
    return render(request, 'rotinas/home.html', context)

def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'rotinas/cadastro.html', {'form': form})

@login_required
def criar_atividade(request):
    """
    Esta view controla a criação de uma nova atividade.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'rotinas/criar_atividade.html', {'form': form})

