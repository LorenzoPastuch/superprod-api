from rest_framework import serializers
from cadastros.models.atributo import Atributo
from cadastros.serializers.empresa_serializer import EmpresaSerializer

class AtributoSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    class Meta:
        model = Atributo
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        empresa = representation.pop('empresa', None)
        representation['empresa'] = empresa
        return representation