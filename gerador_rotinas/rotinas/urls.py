from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rotas do App
    path('', views.home, name='home'),
    path('criar/', views.criar_atividade, name='criar_atividade'),
    
    # Rotas de Autenticação
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='rotinas/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rotina/criar/', views.criar_rotina, name='criar_rotina'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]