from django.db import models
from cadastros.models.atributo import Atributo
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.empresa import Empresa

class ProducaoPcp(models.Model):
    STATUS = [
        ('FILA P/ PRODUZIR', 'FILA P/ PRODUZIR'),
        ('EM PRODUÇÃO', 'EM PRODUÇÃO'),
        ('FINALIZADA', 'FINALIZADA'),
        ('NÃO FINALIZADA', 'NÃO FINALIZADA')
    ]

    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)

    arte = models.CharField(max_length=100, blank=True, null=True)
    pedido = models.CharField(max_length=10, blank=True, null=True)
    falta = models.IntegerField(blank=True, null=True)
    saida = models.DateTimeField(null=True, blank=True)

    unidades = models.IntegerField()
    kilogramas = models.DecimalField(max_digits=10, decimal_places=1)
    ordem = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS)
    maquina = models.ForeignKey(MaquinaPcp, on_delete=models.CASCADE)

    horainicial = models.DateTimeField(null=True, blank=True)
    horafinal = models.DateTimeField(null=True, blank=True)
    qnt_produzida = models.IntegerField(null=True, blank=True)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)