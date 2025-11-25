from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),
    
    #Usuário
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='rotinas/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    #Rotinas
    path('rotina/criar/', views.criar_rotina, name='criar_rotina'),
    path('rotina/<int:rotina_id>/editar/', views.editar_rotina, name='editar_rotina'),
    path('rotina/<int:rotina_id>/deletar/', views.deletar_rotina, name='deletar_rotina'),
    path('rotina/<int:rotina_id>/visualizar/', views.visualizar_rotina, name='visualizar_rotina'),
    
    #Categoria 
    path('categoria/<int:categoria_id>/', views.home, name='home_filtrada'),

    path('rotina/<int:rotina_id>/', views.visualizar_rotina, name='visualizar_rotina'),
    path('rotina/<int:rotina_id>/atividade/criar/', views.criar_atividade, name='criar_atividade'),
    path('atividade/<int:atividade_id>/editar/', views.editar_atividade, name='editar_atividade'),
    path('atividade/<int:atividade_id>/excluir/', views.excluir_atividade, name='excluir_atividade'),

    path('setup/', views.setup_inicial, name='setup_inicial'),

    path('atividades/reordenar/', views.reordenar_atividades, name='reordenar_atividades'),

]