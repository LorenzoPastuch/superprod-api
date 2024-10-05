from rest_framework import serializers
from cadastros.models.colaborador import Colaborador
from cadastros.serializers.empresa_serializer import EmpresaSerializer

class ColaboradorSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    class Meta:
        model = Colaborador
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        empresa = representation.pop('empresa', None)
        representation['empresa'] = empresa
        return representation