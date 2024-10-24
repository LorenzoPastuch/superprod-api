from rest_framework import serializers
from cadastros.models.produto import Produto
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa

class ProdutoSerializer(serializers.ModelSerializer):
    material = serializers.ChoiceField(choices=Produto.MATERIAIS)
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'sku', 'peso', 'material', 'uncaixa', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        produto = Produto.objects.create(empresa=empresa_ativa, **validated_data)
        return produto

