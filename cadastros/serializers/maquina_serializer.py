from rest_framework import serializers
from cadastros.models.maquina import Maquina, MoldeMaquina
from cadastros.models.molde import Molde
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.serializers.molde_serializer import MoldeSerializer

class MoldeMaquinaSerializer(serializers.ModelSerializer):
    molde = MoldeSerializer()
    class Meta:
        model = MoldeMaquina
        fields = ['molde']

class MaquinaSerializer(serializers.ModelSerializer):
    moldes = serializers.SerializerMethodField()
    class Meta:
        model = Maquina
        fields = ['id', 'nome', 'numero', 'peso', 'status', 'moldes']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        maquina = Maquina.objects.create(empresa=empresa_ativa, **validated_data)

        moldes_data = self.context['request'].data.get('moldes', [])

        for molde in moldes_data:
            molde = Molde.objects.get(id=molde['id'])
            MoldeMaquina.objects.create(
                maquina=maquina,
                molde=molde                
            )
        return maquina

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Remover moldes da validação
        moldes_data = self.context['request'].data.get('moldes', [])

        # Atualizar dados da máquina
        instance.nome = validated_data.get('nome', instance.nome)
        instance.numero = validated_data.get('numero', instance.numero)
        instance.peso = validated_data.get('peso', instance.peso)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Atualizar moldes associados
        MoldeMaquina.objects.filter(maquina=instance).delete()
        for molde in moldes_data:
            molde_instance = Molde.objects.get(id=molde['id'])
            MoldeMaquina.objects.create(maquina=instance, molde=molde_instance)

        return instance
    
    def get_moldes(self, obj):
        moldes = obj.moldemaquina_set.all()
        return MoldeSerializer([ue.molde for ue in moldes], many=True).data