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
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]