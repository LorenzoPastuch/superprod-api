from rest_framework import serializers
from pcp.models.producao_pcp import ProducaoPcp
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.atributo import Atributo
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.atributo_serializer import AtributoSerializer
import math


class ProducaoPcpSerializer(serializers.ModelSerializer):
    atributo =  serializers.SerializerMethodField()
    class Meta:
        model = ProducaoPcp
        fields = ['id', 'atributo', 'quantidade', 'ordem', 'caixas', 'status', 'maquina']
        read_only_fields =['caixas']

    def create(self, validate_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        maquina = self.context['request'].data.get('maquina')
        atributo = self.context['request'].data.get('atributo', {}).get('id')
        quantidade = self.context['request'].data.get('quantidade')
        status = self.context['request'].data.get('status')
        ordem = self.context['request'].data.get('ordem')

        produto = MaquinaPcp.objects.get(id=maquina).produto
        caixas = math.ceil(quantidade/produto.uncaixa)

        producao_pcp = ProducaoPcp.objects.create(
            maquina = MaquinaPcp.objects.get(id=maquina),
            atributo = Atributo.objects.get(id=atributo),
            quantidade = quantidade, 
            status = status,
            ordem = ordem,
            caixas=caixas,
            empresa=empresa_ativa
        )
        return producao_pcp
    
    def update(self, instance, validate_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        maquina = self.context['request'].data.get('maquina', instance.maquina)
        atributo = self.context['request'].data.get('atributo', {}).get('id', instance.atributo.id)
        quantidade = self.context['request'].data.get('quantidade', instance.quantidade)
        status = self.context['request'].data.get('status', instance.status)
        ordem = self.context['request'].data.get('ordem', instance.ordem)

        produto = MaquinaPcp.objects.get(id=maquina).produto
        caixas = math.ceil(quantidade/produto.uncaixa)

        instance.empresa = empresa_ativa
        instance.maquina = MaquinaPcp.objects.get(id=maquina)
        instance.atributo = Atributo.objects.get(id=atributo)
        instance.quantidade = quantidade
        instance.ordem = ordem
        instance.caixas = caixas
        instance.status = status

        instance.save()

        return instance
 
    def get_atributo(self, obj):
        return AtributoSerializer(obj.atributo).data