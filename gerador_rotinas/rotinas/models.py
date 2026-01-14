from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.templatetags.static import static

class Categoria(models.Model):
    nome = models.CharField(max_length=50) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'usuario'],
                name='unique_categoria_por_usuario'
            )
        ]

    def __str__(self):
        if self.usuario:
            return f"{self.nome}  "
        return f"{self.nome} (Global)"

    @property 
    def icone_lucide(self):

        from django.templatetags.static import static

        mapa_icones = {

            'Higiene Pessoal': 'shower-head',
            'Alimentação': 'utensils',
            'Escola/Estudos': 'graduation-cap',
            'Lazer': 'gamepad-2',
            'Sono/Descanso': 'moon',
            'Tarefas Domésticas': 'home',
        }

        return mapa_icones.get(self.nome, 'folder-open')
    
class Rotina(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=False 
    )

    pictograma_padrao = models.CharField(max_length=255, blank=True, null=True)
    pictograma_upload = models.ImageField(upload_to='pictogramas_rotina/', blank=True, null=True)

    def __str__(self):
        return self.titulo

def pictograma_url(self):
    # 1. Se tem arquivo físico que o usuário subiu, usa a URL de MEDIA
    if self.pictograma_upload:
        try:
            return self.pictograma_upload.url
        except:
            pass

    # 2. Se não tem upload, ele PRECISA usar o caminho do static que está no banco
    if self.pictograma_padrao:
        # Garante que o caminho não tenha barras extras e usa a pasta static
        caminho = str(self.pictograma_padrao).strip()
        return static(caminho)

    # 3. Fallback se o banco estiver vazio
    return static("pictogramas_padrao/placeholder.png")

class Atividade(models.Model):

    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE, related_name='atividades')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    pictograma = models.ImageField(upload_to='pictogramas_atividades/', blank=True, null=True)
    pictograma_padrao = models.CharField(max_length=255, blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['ordem']

    @property
    def pictograma_url(self):
        if self.pictograma and hasattr(self.pictograma, 'url'):
            return self.pictograma.url
        
        if self.pictograma_padrao:
            return static(self.pictograma_padrao)
        
        return static('pictogramas_padrao/placeholder.png')