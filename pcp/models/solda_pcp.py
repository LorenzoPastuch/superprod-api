from django.db import models
from cadastros.models.atributo import Atributo
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.empresa import Empresa

class SoldaPcp(models.Model):
    STATUS = [
        ('FILA P/ PRODUZIR', 'FILA P/ PRODUZIR'),
        ('EM PRODUÇÃO', 'EM PRODUÇÃO'),
        ('FINALIZADA', 'FINALIZADA'),
        ('NÃO FINALIZADA', 'NÃO FINALIZADA')
    ]

    cor_1 = models.ForeignKey(Atributo, on_delete=models.CASCADE, related_name='soldapcp_cor1')
    cor_2 = models.ForeignKey(Atributo, on_delete=models.CASCADE, related_name='soldapcp_cor2')
    quantidade = models.IntegerField()
    ordem = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS)
    maquina = models.ForeignKey(MaquinaPcp, on_delete=models.CASCADE)

    horainicial = models.DateTimeField(null=True, blank=True)
    horafinal = models.DateTimeField(null=True, blank=True)
    qnt_produzida = models.IntegerField(null=True, blank=True)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)