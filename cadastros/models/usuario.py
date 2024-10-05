from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .empresa import Empresa

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    status = models.BooleanField(default=True)
    empresaativa = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.usuario.username

class UsuarioEmpresa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    empresapadrao = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.nome} ({'Padrão' if self.empresapadrao else 'Não padrão'})"

