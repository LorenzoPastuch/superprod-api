from rest_framework import serializers
from cadastros.models.producao import Producao

class ProducaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producao
        fields = '__all__'