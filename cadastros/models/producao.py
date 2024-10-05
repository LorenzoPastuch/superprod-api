from django.db import models

class Producao(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    horainicial = models.TimeField(auto_now_add=True)
    horafinal = models.TimeField(auto_now_add=True)
    operador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='operador')
    embalador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='embalador')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    maquina = models.ForeignKey('Maquina', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    atributo = models.ForeignKey('Atributo', on_delete=models.CASCADE)
    perda = models.FloatField()
    motivoperda = models.CharField(max_length=100)
    ciclo = models.FloatField()
    lote = models.CharField(max_length=100)
    observacao = models.TextField()
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    
