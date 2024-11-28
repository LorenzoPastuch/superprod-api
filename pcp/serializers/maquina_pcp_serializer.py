from rest_framework import serializers
from pcp.models.maquina_pcp import MaquinaPcp
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.models.maquina import Maquina
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.maquina_serializer import MaquinaSerializer
from pcp.models.producao_pcp import ProducaoPcp
from pcp.models.solda_pcp import SoldaPcp
from pcp.utils import emitir_atualizacao_producao
import time

class MaquinaPcpSerializer(serializers.ModelSerializer):
    atributo =  serializers.SerializerMethodField()
    arte =  serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()
    maquina = serializers.SerializerMethodField()
    cor_1 = serializers.SerializerMethodField()
    cor_2 = serializers.SerializerMethodField()

    class Meta:
        model = MaquinaPcp
        fields = ['id', 'atributo', 'arte', 'cor_1', 'cor_2', 'produto', 'status', 'prioridade', 'maquina']

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

        time.sleep(0.5) #soluçao temporaria para atualizar corretamente o websocket

        serializer = MaquinaPcpSerializer(instance)
        emitir_atualizacao_producao(serializer)

        return instance

    def get_atributo(self, obj):
        maquina_id = obj.maquina.id
        producao = ProducaoPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.atributo.nome if producao else None
    
    def get_arte(self, obj):
        maquina_id = obj.maquina.id
        producao = ProducaoPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.arte if producao else None
    
    def get_cor_1(self, obj):
        maquina_id = obj.maquina.id
        producao = SoldaPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.cor_1.nome if producao else None

    def get_cor_2(self, obj):
        maquina_id = obj.maquina.id
        producao = SoldaPcp.objects.filter(status='EM PRODUÇÃO', maquina=maquina_id).first()
        return producao.cor_2.nome if producao else None
    
    def get_produto(self, obj):
        produto = obj.produto
        return {"id": produto.id, "nome": produto.nome}
    
    def get_maquina(self, obj):
        maquina = obj.maquina
        return {"id": maquina.id, "nome": maquina.nome, "numero": maquina.numero}
