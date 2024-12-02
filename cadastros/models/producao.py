from django.db import models

class Producao(models.Model):
    data = models.DateTimeField()
    horainicial = models.CharField(max_length=100, blank=True, null=True)
    horafinal = models.CharField(max_length=100, blank=True, null=True)
    operador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='operador')
    embalador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='embalador')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    maquina = models.ForeignKey('Maquina', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    atributo = models.ForeignKey('Atributo', on_delete=models.CASCADE)
    perda = models.FloatField(null=True)
    motivoperda = models.CharField(max_length=100, blank=True, null=True)
    trocacor = models.FloatField(null=True)
    ciclo = models.FloatField(null=True)
    lote = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    
