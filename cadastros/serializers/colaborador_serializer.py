from rest_framework import serializers
from cadastros.models.colaborador import Colaborador

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = '__all__'