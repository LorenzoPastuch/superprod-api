from django.db import models
from cadastros.models.atributo import Atributo
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.empresa import Empresa

class ProducaoPcp(models.Model):
    STATUS = [
        ('FILA P/ PRODUZIR', 'FILA P/ PRODUZIR'),
        ('EM PRODUÇÃO', 'EM PRODUÇÃO'),
        ('FINALIZADA', 'FINALIZADA')
    ]
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    # caixas = models.IntegerField()
    ordem = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS)
    maquina = models.ForeignKey(MaquinaPcp, on_delete=models.CASCADE)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)