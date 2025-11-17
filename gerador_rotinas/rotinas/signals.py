from django.db.models.signals import post_migrate 
from django.dispatch import receiver 
from .models import Categoria 

#@receiver (post_migrate)
#def  categorias_padrao (sender, **kwargs): 
#
 #   if sender.name == 'rotinas': 
 #       categorias_padrao = ['Cotidiano', 'Estudo']
  #  
   #     for nome_categoria in categorias_padrao: 
#
 #           Categoria.objects.get_or_create(nome=nome_categoria)
  #          print(f'Categoria "{nome_categoria}" verificada/criada.')