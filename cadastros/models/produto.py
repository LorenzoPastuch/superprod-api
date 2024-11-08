from django.db import models
from .empresa import Empresa

class Produto(models.Model):
    MATERIAIS = [
        ('PS', 'Poliestireno'),
        ('PP', 'Polipropileno'),
        ('PEBD', 'Polietileno de Baixa Densidade'),
        ('TPE', 'Termoplastico Expandido'),
    ]
    nome = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=3)
    material = models.CharField(max_length=100, choices=MATERIAIS)
    embalagem = models.CharField(max_length=10)
    uncaixa = models.IntegerField()
    unembalagem = models.IntegerField()
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
