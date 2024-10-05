from django.db import models
from .empresa import Empresa

class Maquina(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.IntegerField()
    peso = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class MoldeMaquina(models.Model):
    maquina = models.ForeignKey('Maquina', on_delete=models.CASCADE)
    molde = models.ForeignKey('Molde', on_delete=models.CASCADE)

    def __str__(self):
        return self.molde.nome + ' - ' + self.maquina.nome