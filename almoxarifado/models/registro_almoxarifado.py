from django.db import models
from cadastros.models.empresa import Empresa
from cadastros.models.insumo import Insumo

class RegistroAlmoxarifado(models.Model):
    TIPO_MOVIMENTACAO = [
        ('RETIRADA', 'RETIRADA'),
        ('DEVOLUÇÃO', 'DEVOLUÇÃO')
    ]

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    datagravacao = models.DateTimeField()
    usuariogravacao = models.CharField(max_length=100, blank=True)
    tipo_movimentacao = models.CharField(max_length=100, choices=TIPO_MOVIMENTACAO)
    statuswms = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

