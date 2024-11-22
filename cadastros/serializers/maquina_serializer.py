from rest_framework import serializers
from cadastros.models.maquina import Maquina, MoldeMaquina
from cadastros.models.molde import Molde
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.serializers.molde_serializer import MoldeSerializer
from cadastros.serializers.log_cadastro_serializer import LogCadastroMixin
from cadastros.models.log_cadastro import Log_cadastro
from pcp.models.maquina_pcp import MaquinaPcp

class MoldeMaquinaSerializer(serializers.ModelSerializer):
    molde = MoldeSerializer()
    class Meta:
        model = MoldeMaquina
        fields = ['molde']

class MaquinaSerializer(LogCadastroMixin, serializers.ModelSerializer):
    moldes = serializers.SerializerMethodField()
    usuariogravacao = serializers.SerializerMethodField()
    datagravacao = serializers.SerializerMethodField()
    class Meta:
        model = Maquina
        fields = ['id', 'nome', 'numero', 'peso', 'status', 'moldes', 'usuariogravacao', 'datagravacao']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        maquina = Maquina.objects.create(empresa=empresa_ativa, **validated_data)
        MaquinaPcp.objects.create(
            status='PARADA',
            empresa=empresa_ativa,
            maquina=maquina,
            produto=Produto.objects.get(id=1),
            prioridade=False
        )

        moldes_data = self.context['request'].data.get('moldes', [])

        for molde in moldes_data:
            molde = Molde.objects.get(id=molde['id'])
            MoldeMaquina.objects.create(
                maquina=maquina,
                molde=molde                
            )

        self.registrar_log(
            comando=f"Criar Maquina de ID {maquina.id}",
            usuario=user,
            instance=maquina,
        )    
        return maquina

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Remover moldes da validação
        moldes_data = self.context['request'].data.get('moldes', [])

        # Atualizar dados da máquina
        instance.nome = validated_data.get('nome', instance.nome)
        instance.numero = validated_data.get('numero', instance.numero)
        instance.peso = validated_data.get('peso', instance.peso)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if (instance.status==False):
            print('aqui')
            MaquinaPcp.objects.filter(maquina=instance).delete()
        elif not MaquinaPcp.objects.filter(maquina=instance).exists():
            print('aqui nao')
            MaquinaPcp.objects.create(
                status='PARADA',
                empresa=instance.empresa,
                maquina=instance,
                produto=Produto.objects.get(id=1),
                prioridade=False
            )
        # Atualizar moldes associados
        MoldeMaquina.objects.filter(maquina=instance).delete()
        for molde in moldes_data:
            molde_instance = Molde.objects.get(id=molde['id'])
            MoldeMaquina.objects.create(maquina=instance, molde=molde_instance)

        self.registrar_log(
            comando=f"Editar Maquina de ID {instance.id}",
            usuario=user,
            instance=instance,
        )
        return instance
    
    def get_moldes(self, obj):
        moldes = obj.moldemaquina_set.all()
        return MoldeSerializer([ue.molde for ue in moldes], many=True).data
    
    def get_usuariogravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(maquina=obj).order_by('-datagravacao').first()
        if log:
            return log.usuariogravacao
        return None

    def get_datagravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(maquina=obj).order_by('-datagravacao').first()
        if log:
            return log.datagravacao
        return None