from rest_framework import serializers
from pcp.models.embaladores_pcp import EmbaladoresPcp
from cadastros.models.colaborador import Colaborador
from cadastros.models.maquina import Maquina
from cadastros.serializers.colaborador_serializer import ColaboradorSerializer
from pcp.serializers.maquina_pcp_serializer import MaquinaPcpSerializer
from pcp.models.maquina_pcp import MaquinaPcp

class EmbaladoresPcpSerializer(serializers.ModelSerializer):
    maquina = serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()
    embalador = ColaboradorSerializer()
    status = serializers.SerializerMethodField()
    nome_embalador = serializers.SerializerMethodField()

    class Meta:
        model = EmbaladoresPcp
        fields = ['id', 'maquina', 'produto', 'status', 'nome_embalador', 'embalador', 'setor']


    def update(self, instance, validated_data):

        maquina = self.context['request'].data.get('maquina',{}).get('id', instance.maquina.id)
        embalador = self.context['request'].data.get('embalador',{}).get('id', instance.embalador.id)
        setor = self.context['request'].data.get('setor', instance.setor)

        instance.embalador = Colaborador.objects.get(id=embalador)
        instance.maquina = MaquinaPcp.objects.get(id=maquina)
        instance.setor = setor

        instance.save()
        return instance

    def get_maquina(self, obj):
        return MaquinaPcpSerializer(obj.maquina).data
    
    def get_produto(self, obj):
        return obj.maquina.produto.nome 
    
    def get_status(self, obj):
        return obj.maquina.status
    
    def get_nome_embalador(self, obj):
        embalador = obj.embalador
        return embalador.nome if embalador else None