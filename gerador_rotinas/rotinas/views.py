from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, logout
from .models import Rotina
from .forms import RotinaForm
from usuarios.forms import CustomUserCreationForm, UserProfileForm

@login_required
def home(request):
    lista_de_rotinas = Rotina.objects.filter(usuario=request.user).order_by('ordem')
    contexto = {'rotinas': lista_de_rotinas}
    return render(request, 'rotinas/home.html', contexto)

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

@login_required # Garante que apenas usuários logados possam criar rotinas
def criar_rotina(request):
    """
    Esta view controla a criação de uma nova rotina.
    """
    if request.method == 'POST':
        # Cria uma instância do formulário com os dados enviados (POST) e arquivos (FILES)
        form = RotinaForm(request.POST, request.FILES)
        if form.is_valid():
            # Não salva no banco de dados ainda, apenas cria o objeto em memória
            nova_rotina = form.save(commit=False)
            
            # Associa a rotina ao usuário que está logado
            nova_rotina.usuario = request.user 
            
            # Agora sim, salva a rotina completa no banco de dados
            nova_rotina.save()
            
            # Redireciona para a página inicial (ou para uma página de "sucesso")
            return redirect('home')
    else:
        # Se não for um POST, apenas cria um formulário em branco
        form = RotinaForm()
    
    # Renderiza o template, passando o formulário como contexto
    return render(request, 'rotinas/criar_rotina.html', {'form': form})

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

