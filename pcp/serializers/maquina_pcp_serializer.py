from rest_framework import serializers
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.models.maquina import Maquina
from cadastros.models.atributo import Atributo
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.maquina_serializer import MaquinaSerializer
from pcp.models.producao_pcp import ProducaoPcp


class MaquinaPcpSerializer(serializers.ModelSerializer):
    atributo =  serializers.SerializerMethodField()
    arte =  serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()
    maquina = serializers.SerializerMethodField()
    class Meta:
        model = MaquinaPcp
        fields = ['id', 'atributo', 'arte', 'produto', 'status', 'prioridade', 'maquina']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        produto = self.context['request'].data.get('produto', {}).get('id', instance.produto.id)
        status = self.context['request'].data.get('status', instance.status)
        prioridade = self.context['request'].data.get('prioridade', instance.prioridade)
        maquina = self.context['request'].data.get('maquina',{}).get('id', instance.maquina.id)

        instance.empresa = empresa_ativa
        instance.produto = Produto.objects.get(id=produto)
        instance.maquina = Maquina.objects.get(id=maquina)
        instance.status = status
        instance.prioridade = prioridade

        instance.save()
        return instance

    def get_atributo(self, obj):
        maquina_id = obj.maquina.id
        producao = ProducaoPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.atributo.nome if producao else None
    
    def get_arte(self, obj):
        maquina_id = obj.maquina.id
        producao = ProducaoPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.arte if producao else None
    
    def get_produto(self, obj):
        return ProdutoSerializer(obj.produto).data
    
    def get_maquina(self, obj):
        return MaquinaSerializer(obj.maquina).data