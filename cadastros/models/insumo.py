from django.db import models
from .empresa import Empresa

class Insumo(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    classe = models.CharField(max_length=10)
    codigowms = models.IntegerField()
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)


