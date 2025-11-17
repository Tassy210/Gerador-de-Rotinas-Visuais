from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.templatetags.static import static

class Categoria(models.Model):
    # --- CAMPO DE PICTOGRAMA REMOVIDO DAQUI ---
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
            return f"{self.nome} ({self.usuario.username})"
        return f"{self.nome} (Global)"
    
    # --- PROPERTY DE PICTOGRAMA REMOVIDA DAQUI ---

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

    # --- CAMPOS DE PICTOGRAMA MOVIDOS PARA CÁ ---
    pictograma_padrao = models.CharField(max_length=255, blank=True, null=True)
    pictograma_upload = models.ImageField(upload_to='pictogramas_rotina/', blank=True, null=True)

    def __str__(self):
        return self.titulo

    @property
    def pictograma_url(self):
        """
        CORRIGIDO: Retorna a URL do pictograma da PRÓPRIA ROTINA.
        """
        # 1. Prioriza o upload do usuário
        if self.pictograma_upload and hasattr(self.pictograma_upload, 'url'):
            return self.pictograma_upload.url
        
        # 2. Se não houver, usa o pictograma padrão
        if self.pictograma_padrao: 
            return static(self.pictograma_padrao)
        
        # 3. Se não houver nada, usa um placeholder
        return static("pictogramas_padrao/placeholder.png")

    class Meta:
        pass 

class Atividade(models.Model):
    # --- ESTE MODELO NÃO MUDA NADA, JÁ ESTAVA CORRETO ---
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