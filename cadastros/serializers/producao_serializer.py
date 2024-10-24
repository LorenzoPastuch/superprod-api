from rest_framework import serializers
from cadastros.models.producao import Producao
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.colaborador import Colaborador
from cadastros.models.produto import Produto
from cadastros.models.maquina import Maquina
from cadastros.models.atributo import Atributo
from cadastros.serializers.atributo_serializer import AtributoSerializer
from cadastros.serializers.colaborador_serializer import ColaboradorSerializer
from cadastros.serializers.maquina_serializer import MaquinaSerializer
from cadastros.serializers.produto_serializer import ProdutoSerializer

class ProducaoSerializer(serializers.ModelSerializer):
    operador = serializers.SerializerMethodField()
    embalador = serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()
    maquina = serializers.SerializerMethodField()
    atributo = serializers.SerializerMethodField()

    class Meta:
        model = Producao
        fields = ['id', 'data', 'horainicial', 'horafinal', 'operador', 'embalador', 'produto', 'maquina', 'quantidade', 'atributo', 'perda', 'motivoperda', 'ciclo', 'lote', 'observacao', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        data = self.context['request'].data.get('data')
        operador = self.context['request'].data.get('operador', {})
        embalador = self.context['request'].data.get('embalador', {})
        produto = self.context['request'].data.get('produto', {})
        maquina = self.context['request'].data.get('maquina', {})
        atributo = self.context['request'].data.get('atributo', {})
        quantidade = self.context['request'].data.get('quantidade')
        horainicial = self.context['request'].data.get('horainicial')
        horafinal = self.context['request'].data.get('horafinal')
        perda = self.context['request'].data.get('perda')
        motivoperda = self.context['request'].data.get('motivoperda')
        ciclo = self.context['request'].data.get('ciclo')
        lote = self.context['request'].data.get('lote')
        observacao = self.context['request'].data.get('observacao')
        status = self.context['request'].data.get('status')
        

        producao = Producao.objects.create(
            empresa=empresa_ativa,
            operador = Colaborador.objects.get(id=operador['id']),
            embalador = Colaborador.objects.get(id=embalador['id']),
            produto = Produto.objects.get(id=produto['id']),
            maquina = Maquina.objects.get(id=maquina['id']),  
            atributo = Atributo.objects.get(id=atributo['id']),
            quantidade = quantidade,
            data = data,
            horainicial = horainicial,
            horafinal = horafinal,
            perda = perda,
            motivoperda = motivoperda,
            ciclo = ciclo,
            lote = lote,
            observacao = observacao,
            status = status,
        )
        return producao

    def get_operador(self, obj):
        return ColaboradorSerializer(obj.operador).data
    
    def get_embalador(self, obj):
        return ColaboradorSerializer(obj.embalador).data
    
    def get_produto(self, obj):
        return ProdutoSerializer(obj.produto).data
    
    def get_maquina(self, obj):
        return MaquinaSerializer(obj.maquina).data
    
    def get_atributo(self, obj):
        return AtributoSerializer(obj.atributo).data