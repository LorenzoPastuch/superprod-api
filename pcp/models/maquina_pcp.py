from django.db import models
from cadastros.models.maquina import Maquina
from cadastros.models.produto import Produto
from cadastros.models.empresa import Empresa

class MaquinaPcp(models.Model):
    STATUS = [
        ('PARADA', 'PARADA'),
        ('EM PRODUÇÃO', 'EM PRODUÇÃO'),
        ('TROCA DE MOLDE', 'TROCA DE MOLDE')
    ]
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    prioridade = models.BooleanField(default=False)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)