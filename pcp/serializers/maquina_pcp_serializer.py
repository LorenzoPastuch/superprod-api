from rest_framework import serializers
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.models.maquina import Maquina
from cadastros.models.atributo import Atributo
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.atributo_serializer import AtributoSerializer
from pcp.models.producao_pcp import ProducaoPcp


class MaquinaPcpSerializer(serializers.ModelSerializer):
    atributo =  serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()
    class Meta:
        model = MaquinaPcp
        fields = ['id', 'atributo', 'produto', 'status', 'maquina']

    # def create(self, validate_data):
    #     request = self.context.get('request')
    #     user = request.user

    #     perfil = Perfil.objects.get(usuario=user)
    #     id_empresa_ativa = perfil.empresaativa
    #     empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

    #     maquina = self.context['request'].data.get('maquina', {})
    #     atributo = self.context['request'].data.get('atributo', {})
    #     quantidade = self.context['request'].data.get('quantidade')
    #     status = self.context['request'].data.get('status')
    #     ordem = self.context['request'].data.get('status')

    #     producao_pcp = ProducaoPcp.objects.create(
    #         maquina = Maquina.objects.get(id=maquina['id']),
    #         atributo = Atributo.objects.get(id=atributo['id']),
    #         quantidade = quantidade, 
    #         status = status,
    #         ordem = ordem,
    #         empresa_ativa=empresa_ativa
    #     )
    #     return producao_pcp
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        produto = self.context['request'].data.get('produto', {}).get('id', instance.produto.id)
        status = self.context['request'].data.get('status', instance.status)
        maquina = self.context['request'].data.get('maquina', instance.maquina)

        instance.empresa = empresa_ativa
        instance.produto = Produto.objects.get(id=produto)
        instance.maquina = Maquina.objects.get(id=maquina)
        instance.status = status

        instance.save()
        return instance

    def get_atributo(self, obj):
        maquina_id = obj.maquina.id
        producao = ProducaoPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.atributo.nome if producao else None
    
    def get_produto(self, obj):
        return ProdutoSerializer(obj.produto).data