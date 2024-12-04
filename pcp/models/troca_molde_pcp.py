from django.db import models
from cadastros.models.maquina import Maquina
from cadastros.models.molde import Molde

class TrocaMoldePcp(models.Model):

    STATUST = [
        ('NÃO INICIADA', 'NÃO INICIADA'),
        ('EM EXECUÇÃO', 'EM EXECUÇÃO'),
        ('CONCLUÍDA', 'CONCLUÍDA')
    ]

    STATUSM = [
        ('PRODUZIDO', 'PRODUZIDO'),
        ('EM PRODUÇÃO', 'EM PRODUÇÃO'),
        ('FILA DE PRODUÇÃO', 'FILA DE PRODUÇÃO'),
    ]

    injetora = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    molde_maquina = models.ForeignKey(Molde, on_delete=models.CASCADE, related_name='trocamoldepcp_molde_maquina')
    proximo_molde = models.ForeignKey(Molde, on_delete=models.CASCADE, related_name='trocamolde_proximo_molde')
    status_molde = models.CharField(max_length=50, choices=STATUSM)
    status_troca = models.CharField(max_length=50, choices=STATUST)
    data_prevista = models.DateTimeField(null=True, blank=True)
    data_realizada = models.DateTimeField(null=True, blank=True)
    observacoes = models.CharField(max_length=100, null=True, blank=True)
    ordem = models.IntegerField()