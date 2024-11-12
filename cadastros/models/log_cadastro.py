from django.db import models

class Log_cadastro(models.Model):
    comando = models.CharField(max_length=100)
    datagravacao = models.DateTimeField()
    usuariogravacao = models.CharField(max_length=100)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True)
    maquina = models.ForeignKey('Maquina', on_delete=models.CASCADE, null=True)
    molde = models.ForeignKey('Molde', on_delete=models.CASCADE, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE, null=True)
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, null=True)
    atributo = models.ForeignKey('Atributo', on_delete=models.CASCADE, null=True)
    producao = models.ForeignKey('Producao', on_delete=models.CASCADE, null=True)
    insumo = models.ForeignKey('Insumo', on_delete=models.CASCADE, null=True)

    