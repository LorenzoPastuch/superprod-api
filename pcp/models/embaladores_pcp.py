from django.db import models
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.colaborador import Colaborador

class EmbaladoresPcp(models.Model):

    SETORES = [
        ('INJETORA', 'INJETORA'),
        ('SOLDA', 'SOLDA'),
        ('CANUDOS', 'CANUDOS'),
    ]

    maquina = models.ForeignKey(MaquinaPcp, on_delete=models.CASCADE)
    embalador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    setor = models.CharField(max_length=100, choices=SETORES)