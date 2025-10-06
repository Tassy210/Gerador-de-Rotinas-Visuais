from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, logout
from .models import Atividade
from usuarios.forms import CustomUserCreationForm, UserProfileForm

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

def criar_rotina(request):

    return render(request, 'rotinas/criar_rotina.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Passamos 'instance=request.user' para dizer ao form qual usuário estamos editando
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Adiciona uma mensagem de sucesso
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home') # Ou para a mesma página: redirect('editar_perfil')
    else:
        # Ao carregar a página pela primeira vez, o form já vem preenchido com os dados do usuário
        form = UserProfileForm(instance=request.user)

    return render(request, 'rotinas/editar_perfil.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

