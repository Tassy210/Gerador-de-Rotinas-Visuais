from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    pictograma_padrao = models.ImageField(upload_to='pictogramas_categoria/', help_text="Pictograma padrão para esta categoria.", blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Rotina(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Atividade(models.Model):
    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE, related_name='atividades')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    pictograma = models.ImageField(upload_to='pictogramas/', blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo