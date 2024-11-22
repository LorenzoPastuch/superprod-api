from rest_framework import serializers
from pcp.models.troca_molde_pcp import TrocaMoldePcp
from cadastros.serializers.maquina_serializer import MaquinaSerializer
from cadastros.serializers.molde_serializer import MoldeSerializer
from cadastros.models.maquina import Maquina
from cadastros.models.molde import Molde

class TrocaMoldePcpSerializer(serializers.ModelSerializer):
    injetora = serializers.SerializerMethodField()
    molde_maquina = serializers.SerializerMethodField()
    proximo_molde = serializers.SerializerMethodField()

    class Meta:
        model = TrocaMoldePcp
        fields = ['id', 'injetora', 'molde_maquina', 'status_molde', 'proximo_molde', 'status_troca', 'data_prevista', 'data_realizada', 'observacoes']

    def create(self, validate_data):

        injetora  = self.context['request'].data.get('injetora', {}).get('id')
        molde_maquina = self.context['request'].data.get('molde_maquina', {}).get('id')
        status_molde = self.context['request'].data.get('status_molde')
        proximo_molde = self.context['request'].data.get('proximo_molde', {}).get('id')
        status_troca = self.context['request'].data.get('status_troca')
        data_prevista = self.context['request'].data.get('data_prevista')
        data_realizada = self.context['request'].data.get('data_realizada')
        observacoes = self.context['request'].data.get('observacoes')

        injetora = Maquina.objects.get(id=injetora)
        molde_maquina = Molde.objects.get(id=molde_maquina)
        proximo_molde = Molde.objects.get(id=proximo_molde)

        trocamolde = TrocaMoldePcp.objects.create(
            injetora=injetora,
            molde_maquina=molde_maquina,
            status_molde=status_molde,
            proximo_molde=proximo_molde,
            status_troca=status_troca,
            data_prevista=data_prevista,
            data_realizada=data_realizada,
            observacoes=observacoes
        )
        return trocamolde
    
    def update(self, instance, validate_data):

        injetora = self.context['request'].data.get('injetora', {}).get('id', instance.injetora.id)
        molde_maquina = self.context['request'].data.get('molde_maquina', {}).get('id', instance.molde_maquina.id)
        status_molde = self.context['request'].data.get('status_molde', instance.status_molde)
        proximo_molde = self.context['request'].data.get('proximo_molde', {}).get('id', instance.proximo_molde.id)
        status_troca = self.context['request'].data.get('status_troca', instance.status_troca)
        data_prevista = self.context['request'].data.get('data_prevista', instance.data_prevista)
        data_realizada = self.context['request'].data.get('data_realizada', instance.data_realizada)
        observacoes = self.context['request'].data.get('observacoes', instance.observacoes)

        injetora = Maquina.objects.get(id=injetora)
        molde_maquina = Molde.objects.get(id=molde_maquina)
        proximo_molde = Molde.objects.get(id=proximo_molde)

        instance.injetora = injetora
        instance.molde_maquina = molde_maquina
        instance.status_molde = status_molde
        instance.proximo_molde = proximo_molde
        instance.status_troca = status_troca
        instance.data_prevista = data_prevista
        instance.data_realizada = data_realizada
        instance.observacoes = observacoes
        instance.save()

        return instance
        
    
    def get_molde_maquina(self, obj):
        return MoldeSerializer(obj.molde_maquina).data
    
    def get_proximo_molde(self, obj):
        return MoldeSerializer(obj.proximo_molde).data
    
    def get_injetora(self, obj):
        return MaquinaSerializer(obj.injetora).data
