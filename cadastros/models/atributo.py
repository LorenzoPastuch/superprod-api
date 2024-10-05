from django.db import models

class Atributo(models.Model):
    nome = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nome