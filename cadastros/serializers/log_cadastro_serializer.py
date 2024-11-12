from django.utils import timezone
from cadastros.models.log_cadastro import Log_cadastro
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.models.molde import Molde
from cadastros.models.atributo import Atributo
from cadastros.models.colaborador import Colaborador
from cadastros.models.maquina import Maquina
from cadastros.models.producao import Producao
from cadastros.models.insumo import Insumo


class LogCadastroMixin:
    
    def registrar_log(self, comando, usuario, instance):

        perfil = Perfil.objects.get(usuario=usuario)
        empresa_ativa = Empresa.objects.get(id=perfil.empresaativa)

        produto = instance if isinstance(instance, Produto) else None
        molde = instance if isinstance(instance, Molde) else None
        maquina = instance if isinstance(instance, Maquina) else None
        colaborador = instance if isinstance(instance, Colaborador) else None
        atributo = instance if isinstance(instance, Atributo) else None
        producao = instance if isinstance(instance, Producao) else None
        insumo = instance if isinstance(instance, Insumo) else None

        Log_cadastro.objects.create(
            comando=comando,
            datagravacao=timezone.now(),
            usuariogravacao=usuario.username,
            empresa=empresa_ativa,
            maquina=maquina,
            molde=molde,
            produto=produto,
            colaborador=colaborador,
            atributo=atributo,
            producao=producao,
            insumo=insumo
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        self.registrar_log(
            comando=f"Criar {instance.__class__.__name__} de ID {instance.id}",
            usuario=self.context['request'].user,
            instance=instance
        )
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.registrar_log(
            comando=f"Alterar {instance.__class__.__name__} de ID {instance.id}",
            usuario=self.context['request'].user,
            instance=instance
        )
        return instance