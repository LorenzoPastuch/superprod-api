from rest_framework import serializers

class PigmentoSerializer(serializers.Serializer):
    cor = serializers.CharField()
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=3)


class InsumosPcpSerializer(serializers.Serializer):
    pigmentos = PigmentoSerializer(many=True)
    tipo_material = serializers.CharField(source='producao__maquina__produto__material')
    tipo_embalagem = serializers.CharField(source='producao__maquina__produto__embalagem')
    produto = serializers.CharField(source='producao__maquina__produto__nome')
    maquina = serializers.IntegerField(source='producao__maquina__id')
    total_caixas = serializers.IntegerField()
    total_qnt_material = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_embalagens = serializers.IntegerField()

