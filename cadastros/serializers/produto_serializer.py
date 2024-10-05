from rest_framework import serializers
from cadastros.models.produto import Produto
from cadastros.serializers.empresa_serializer import EmpresaSerializer

class ProdutoSerializer(serializers.ModelSerializer):
    material = serializers.ChoiceField(choices=Produto.MATERIAIS)
    empresa = EmpresaSerializer(read_only=True)
    class Meta:
        model = Produto
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        empresa = representation.pop('empresa', None)
        representation['empresa'] = empresa
        return representation