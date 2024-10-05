from rest_framework import serializers
from cadastros.models.maquina import Maquina, MoldeMaquina
from cadastros.models.molde import Molde

class MoldeMaquinaSerializer(serializers.ModelSerializer):
    molde = serializers.PrimaryKeyRelatedField(queryset=Molde.objects.all())

    class Meta:
        model = MoldeMaquina
        fields = ['molde']

class MaquinaSerializer(serializers.ModelSerializer):
    moldes = MoldeMaquinaSerializer(source='moldemaquina_set', many=True)
    class Meta:
        model = Maquina
        fields = ['id', 'nome', 'numero', 'peso', 'status', 'empresa', 'moldes']

    def create(self, validated_data):
        moldes = validated_data.pop('moldemaquina_set', [])
        maquina = Maquina.objects.create(**validated_data)
        for molde in moldes:
            MoldeMaquina.objects.create(
                maquina=maquina,
                **molde                
            )
        return maquina
