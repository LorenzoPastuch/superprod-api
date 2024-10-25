from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)
    numero = models.IntegerField()
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome