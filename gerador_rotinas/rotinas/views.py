from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login, logout
from django.db.models import Max  
from django.contrib import messages 
from .models import Rotina, Categoria, Atividade 
from .forms import RotinaForm, CategoriaForm, AtividadeForm
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
    categorias = Categoria.objects.filter(
        Q(usuario=request.user) | Q(usuario__isnull=True)
    ).order_by('nome')

    if categoria_id:
        
        lista_de_rotinas = Rotina.objects.filter(usuario=request.user, categoria_id=categoria_id).order_by('titulo')
    else:
        
        lista_de_rotinas = Rotina.objects.filter(usuario=request.user).order_by('titulo')

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
def deletar_rotina(request, rotina_id):
    rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user) 
    if request.method == 'POST':
        rotina.delete()
        return redirect('home')
    context = { 'rotina': rotina }
    return render(request, 'rotinas/deletar_rotina.html', context)

# --- Views de Atividade (Passos da Rotina) ---

@login_required 
def visualizar_rotina(request, rotina_id): 
    rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user) 
    
    # CORREÇÃO: Precisamos buscar os "passos" (Atividades) desta rotina
    atividades_da_rotina = Atividade.objects.filter(rotina=rotina).order_by('ordem')
    
    context = {
        'rotina': rotina,
        'atividades': atividades_da_rotina # <-- Enviando os passos para o template
    }
    return render(request, 'rotinas/visualizar_rotina.html', context)

@login_required
def criar_atividade(request, rotina_id):
    # CORREÇÃO: Chamada correta da função get_object_or_404
    rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user)

    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES)
        if form.is_valid():
            # CORREÇÃO: Usando commit=False para adicionar dados antes de salvar
            atividade = form.save(commit=False) 
            atividade.rotina = rotina 
            atividade.usuario = request.user 

            # CORREÇÃO: Lógica para calcular a próxima ordem
            max_ordem = Atividade.objects.filter(rotina=rotina).aggregate(Max('ordem'))['ordem__max']
            if max_ordem is not None:
                atividade.ordem = max_ordem + 1
            else:
                atividade.ordem = 1 # É a primeira atividade
            
            atividade.save() # Agora salva no banco

            return redirect('visualizar_rotina', rotina_id=rotina.id)
    else: 
        form = AtividadeForm()

    contexto = {
            'form': form,
            'rotina': rotina 
        }
    return render(request, 'rotinas/criar_atividade.html', contexto)

@login_required
def editar_atividade(request, atividade_id):
    # Garante que a atividade existe E pertence ao usuário logado
    atividade = get_object_or_404(Atividade, id=atividade_id, usuario=request.user)
    rotina_id_para_redirecionar = atividade.rotina.id

    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect('visualizar_rotina', rotina_id=rotina_id_para_redirecionar)
    else:
        form = AtividadeForm(instance=atividade)

    context = {
        'form': form,
        'atividade': atividade,
        'rotina': atividade.rotina
    }
    return render(request, 'rotinas/editar_atividade.html', context)

@login_required
def excluir_atividade(request, atividade_id):
    atividade = get_object_or_404(Atividade, id=atividade_id, usuario=request.user)
    rotina_id_para_redirecionar = atividade.rotina.id
    
    if request.method == 'POST':
        atividade.delete()
        # FUTURA MELHORIA: Reordenar os itens restantes (opcional)
        return redirect('visualizar_rotina', rotina_id=rotina_id_para_redirecionar)

    context = {
        'atividade': atividade,
        'rotina': atividade.rotina
    }
    return render(request, 'rotinas/excluir_atividade.html', context)

# --- Views de Usuário ---

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