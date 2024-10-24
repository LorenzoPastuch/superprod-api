from rest_framework import serializers
from cadastros.models.molde import Molde
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.serializers.produto_serializer import ProdutoSerializer

class MoldeSerializer(serializers.ModelSerializer):
    produto = serializers.SerializerMethodField()
    
    class Meta:
        model = Molde
        fields = ['id', 'nome', 'produto', 'fabricante', 'cavidades', 'ciclo', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)
        
        produto_id = self.context['request'].data.get('produto')
        produto_id = (produto_id['id'])

        produto = Produto.objects.get(id=produto_id)

        molde = Molde.objects.create(empresa=empresa_ativa, produto=produto, **validated_data)
        return molde
    
    def get_produto(self, obj):
        produto = obj.produto
        return ProdutoSerializer(produto).data
