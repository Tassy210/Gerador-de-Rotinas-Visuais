from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, logout
from .models import Rotina, Categoria
from .forms import RotinaForm, CategoriaForm
from usuarios.forms import CustomUserCreationForm, UserProfileForm

@login_required
def home(request, categoria_id=None):

    if request.method == 'POST':

        categoria_form = CategoriaForm(request.POST)
        if categoria_form.is_valid():
            nova_categoria = categoria_form.save(commit=False)
            nova_categoria.usuario = request.user 
            nova_categoria.save()
            return redirect('home')

    categoria_form = CategoriaForm()   

    categorias = Categoria.objects.filter(usuario=request.user).order_by('nome')

    if categoria_id:
        lista_de_rotinas = Rotina.objects.filter(usuario=request.user, categoria_id=categoria_id).order_by('ordem')
    else:
        lista_de_rotinas = Rotina.objects.filter(usuario=request.user).order_by('ordem')

    contexto = {
        'rotinas': lista_de_rotinas,
        'categorias': categorias,
        'categoria_selecionada_id': categoria_id,
        'categoria_form': categoria_form
    }

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

@login_required 
def criar_rotina(request):
    if request.method == 'POST':

        form = RotinaForm(request.POST, request.FILES) 
        if form.is_valid():
            nova_rotina = form.save(commit=False)
            nova_rotina.usuario = request.user 
            nova_rotina.save()
            return redirect('home')
    else:
        form = RotinaForm()
    
    return render(request, 'rotinas/criar_rotina.html', {'form': form})
    
@login_required
def editar_rotina(request, rotina_id):
    rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user)

    if request.method == 'POST':

        form = RotinaForm(request.POST, request.FILES, instance=rotina)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:

        form = RotinaForm(instance=rotina)
    
    contexto = {
        'form': form,
        'rotina': rotina
    }
    return render(request, 'rotinas/editar_rotina.html', contexto)

@login_required 
def deletar_rotina(request, pk):
    
    rotina = get_object_or_404(Rotina, pk=pk, usuario=request.user) 
    
    if request.method == 'POST':
        rotina.delete()
        return redirect('home')

    context = { 'rotina': rotina }
    return render(request, 'rotinas/deletar_rotina.html', context)

@login_required 
def visualizar_rotina(request, pk): 
    
    rotina = get_object_or_404(Rotina, pk=pk, usuario=request.user) 
    context = {
        'rotina': rotina
    }
   
    return render(request, 'rotinas/visualizar_rotina.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
       
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home') 
    else:

        form = UserProfileForm(instance=request.user)

    return render(request, 'rotinas/editar_perfil.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

