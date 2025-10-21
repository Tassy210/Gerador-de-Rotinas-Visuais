from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rota para o painel de administração
    path('admin/', admin.site.urls),
    
    # "Inclui" todas as rotas do seu aplicativo 'rotinas'
    path('', include('rotinas.urls')),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset.html'), 
         name='password_reset'),

    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), 
         name='password_reset_complete'),
]

# Adiciona as rotas para servir arquivos de mídia (imagens) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)