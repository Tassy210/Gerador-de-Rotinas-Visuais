from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rota para o painel de administração
    path('admin/', admin.site.urls),
    
    # "Inclui" todas as rotas do seu aplicativo 'rotinas'
    path('', include('rotinas.urls')),
]

# Adiciona as rotas para servir arquivos de mídia (imagens) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)