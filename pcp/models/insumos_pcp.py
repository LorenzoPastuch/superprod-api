from django.db import models
from pcp.models.producao_pcp import ProducaoPcp

class InsumosPcp(models.Model):

    producao = models.ForeignKey(ProducaoPcp, on_delete=models.CASCADE)
    caixas = models.IntegerField()
    pigmento = models.DecimalField(max_digits=10, decimal_places=3)
    qnt_material = models.DecimalField(max_digits=10, decimal_places=3)
    embalagem = models.IntegerField()

