from django.db import models
from .empresa import Empresa
from .produto import Produto

class Molde(models.Model):
    nome = models.CharField(max_length=100)
    fabricante = models.TextField()
    cavidades = models.IntegerField()
    ciclo = models.DecimalField(max_digits=10, decimal_places=2)
    pesogalho = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.BooleanField(default=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
