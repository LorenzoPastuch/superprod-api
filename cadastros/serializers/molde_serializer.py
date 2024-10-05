from rest_framework import serializers
from cadastros.models.molde import Molde
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.empresa_serializer import EmpresaSerializer


class MoldeSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    
    class Meta:
        model = Molde
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        produto = representation.pop('produto', None)
        empresa = representation.pop('empresa', None)
        representation['produto'] = produto
        representation['empresa'] = empresa
        return representation
    
