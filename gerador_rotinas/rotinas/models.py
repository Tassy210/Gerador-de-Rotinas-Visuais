from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    pictograma_padrao = models.ImageField(upload_to='pictogramas_categoria/', help_text="Pictograma padrão para esta categoria.", blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta: 
            constraints = [
                models.UniqueConstraint(

                    fields=['nome', 'usuario'], 
                    name='unique_categoria_por_usuario'
                )
            ]

    def __str__(self):
        return self.nome

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

    def __str__(self):
        return self.titulo

    @property
    def pictograma_url(self):
        """
        Retorna a URL do pictograma padrão da Categoria associada.
        """
        if self.categoria and self.categoria.pictograma_padrao:
            return self.categoria.pictograma_padrao.url
            

        return '/static/images/placeholder.svg' 

    class Meta:

        pass 

class Atividade(models.Model):

    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE, related_name='atividades')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    pictograma = models.ImageField(upload_to='pictogramas_atividades/', blank=True, null=True) # <-- CORRETO
    ordem = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['ordem'] 