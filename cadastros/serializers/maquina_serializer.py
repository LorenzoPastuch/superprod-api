from rest_framework import serializers
from cadastros.models.maquina import Maquina

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'