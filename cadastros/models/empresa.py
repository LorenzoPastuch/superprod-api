from django.db import models

class Empresa(models.Model):

    razaosocial = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    nomecontato = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    whats = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.razaosocial
    