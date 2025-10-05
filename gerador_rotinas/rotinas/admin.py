from django.contrib import admin
from .models import Rotina, Atividade, Categoria

# Register your models here.
admin.site.register(Rotina)
admin.site.register(Atividade)
admin.site.register(Categoria)