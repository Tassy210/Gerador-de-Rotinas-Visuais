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

# --- MODELOS DE ROTINA PADRÃO ---

MODELOS_DE_ROTINA = {
    'rotina_banho': {
        'titulo_rotina': 'Rotina de Banho (Modelo)',
        'categoria_nome': 'Higiene Pessoal',
        'descricao_rotina': 'Passos para tomar um banho completo.',
        'path_rotina': 'pictogramas_padrao/banho.png',
        'atividades': [
            {'titulo': 'Tirar a roupa', 'ordem': 1, 'path': 'pictogramas_padrao/tirar_roupa.png'},
            {'titulo': 'Ligar o chuveiro', 'ordem': 2, 'path': 'pictogramas_padrao/ligar_chuveiro.png'},
            {'titulo': 'Lavar o cabelo', 'ordem': 3, 'path': 'pictogramas_padrao/lavar_cabelo.png'},
            {'titulo': 'Lavar o corpo', 'ordem': 4, 'path': 'pictogramas_padrao/lavar_corpo.png'},
            {'titulo': 'Desligar o chuveiro', 'ordem': 5, 'path': 'pictogramas_padrao/desligar_chuveiro.png'},
            {'titulo': 'Secar-se com a toalha', 'ordem': 6, 'path': 'pictogramas_padrao/secar_toalha.png'},
            {'titulo': 'Vestir roupa limpa', 'ordem': 7, 'path': 'pictogramas_padrao/vestir_roupa.png'}
        ]
    },
    'rotina_almoco': {
        'titulo_rotina': 'Rotina de Almoço (Modelo)',
        'categoria_nome': 'Alimentação',
        'descricao_rotina': 'Passos para a hora do almoço.',
        'path_rotina': 'pictogramas_padrao/alimentacao.png',
        'atividades': [
            {'titulo': 'Lavar as mãos', 'ordem': 1, 'path': 'pictogramas_padrao/lavar_mao.png'},
            {'titulo': 'Sentar à mesa', 'ordem': 2, 'path': 'pictogramas_padrao/sentar_a_mesa.png'},
            {'titulo': 'Comer', 'ordem': 3, 'path': 'pictogramas_padrao/comer.png'},
            {'titulo': 'Beber', 'ordem': 4, 'path': 'pictogramas_padrao/beber.png'},
            {'titulo': 'Limpar a boca', 'ordem': 5, 'path': 'pictogramas_padrao/limpar_a_boca.png'},
            {'titulo': 'Escovar os dentes', 'ordem': 6, 'path': 'pictogramas_padrao/escovar_os_dentes.png'}
        ]
    }
}

# --- FUNÇÃO HELPER (AUXILIAR) ---

def criar_rotinas_padrao_completas(usuario):
    """
    Cria o conjunto completo de categorias e, se houver, 
    as rotinas-modelo para um novo usuário.
    """
    
    # 1. Cria as Categorias (simples, só com nome)
    # Voltamos ao que era antes
    nomes_padrao = [
        'Higiene Pessoal',
        'Alimentação',
        'Escola/Estudos',
        'Lazer',
        'Tarefas Domésticas',
        'Sono/Descanso'
    ]
    
    categorias_criadas = {}
    for nome_cat in nomes_padrao:
        categoria_obj, criada = Categoria.objects.get_or_create(
            usuario=usuario,
            nome=nome_cat
            # SEM PICTOGRAMA AQUI
        )
        categorias_criadas[nome_cat] = categoria_obj

    # 2. Agora, itera sobre os MODELOS e cria as rotinas
    for chave_modelo, dados_modelo in MODELOS_DE_ROTINA.items():
        
        categoria_mae = categorias_criadas.get(dados_modelo['categoria_nome'])
        
        if categoria_mae:
            # --- CORREÇÃO AQUI ---
            # Agora salvamos o pictograma_padrao na ROTINA
            nova_rotina, criada_rotina = Rotina.objects.get_or_create(
                usuario=usuario,
                titulo=dados_modelo['titulo_rotina'],
                categoria=categoria_mae,
                defaults={
                    'descricao': dados_modelo['descricao_rotina'],
                    # Pega o caminho da imagem da rotina
                    'pictograma_padrao': dados_modelo.get('path_rotina', None) 
                }
            )
            
            if criada_rotina:
                # 3. Cria todas as Atividades (Passos) - Isso não muda
                for passo in dados_modelo['atividades']:
                    Atividade.objects.create(
                        rotina=nova_rotina,
                        usuario=usuario,
                        titulo=passo['titulo'],
                        ordem=passo['ordem'],
                        pictograma_padrao=passo['path']
                    )
# --- VIEWS PRINCIPAIS ---

@login_required
def home(request, categoria_id=None):
    if not Categoria.objects.filter(usuario=request.user).exists() and not request.session.get('setup_concluido', False):
        return redirect('setup_inicial')

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


@login_required 
def visualizar_rotina(request, rotina_id): 
    rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user) 
    
    atividades_da_rotina = Atividade.objects.filter(rotina=rotina).order_by('ordem')
    
    context = {
        'rotina': rotina,
        'atividades': atividades_da_rotina
    }
    return render(request, 'rotinas/visualizar_rotina.html', context)

@login_required
def criar_atividade(request, rotina_id):
    
    rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user)

    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES)
        if form.is_valid():
            
            atividade = form.save(commit=False) 
            atividade.rotina = rotina 
            atividade.usuario = request.user 

            max_ordem = Atividade.objects.filter(rotina=rotina).aggregate(Max('ordem'))['ordem__max']
            if max_ordem is not None:
                atividade.ordem = max_ordem + 1
            else:
                atividade.ordem = 1 
            
            atividade.save() 

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
        return redirect('visualizar_rotina', rotina_id=rotina_id_para_redirecionar)

    context = {
        'atividade': atividade,
        'rotina': atividade.rotina
    }
    return render(request, 'rotinas/excluir_atividade.html', context)

# --- VIEWS DE ONBOARDING E USUÁRIO ---

@login_required
def setup_inicial(request):
    # Se já tiver categorias, manda pra home
    if Categoria.objects.filter(usuario=request.user).exists():
         return redirect('home')

    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        if resposta == 'sim':
            # --- CORREÇÃO AQUI ---
            # Chamando a função correta que cria TUDO
            criar_rotinas_padrao_completas(request.user) 
            messages.success(request, 'Categorias e rotinas padrão criadas com sucesso!')
        else:
            messages.info(request, 'Ok, você pode criar suas categorias manualmente.')

        request.session['setup_concluido'] = True
        return redirect('home')

    return render(request, 'rotinas/setup_inicial.html')

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