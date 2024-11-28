from django.contrib import admin

from cadastros.models.atributo import Atributo
from cadastros.models.colaborador import Colaborador
from cadastros.models.empresa import Empresa
from cadastros.models.insumo import Insumo
from cadastros.models.log_cadastro import Log_cadastro
from cadastros.models.maquina import Maquina
from cadastros.models.molde import Molde
from cadastros.models.producao import Producao
from cadastros.models.produto import Produto
from cadastros.models.usuario import Perfil

# Register your models here.
admin.site.register(Atributo)
admin.site.register(Colaborador)
admin.site.register(Empresa)
admin.site.register(Insumo)
admin.site.register(Log_cadastro)
admin.site.register(Maquina)
admin.site.register(Molde)
admin.site.register(Producao)
admin.site.register(Produto)
admin.site.register(Perfil)