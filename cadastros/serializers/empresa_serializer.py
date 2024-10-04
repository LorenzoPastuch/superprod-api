from rest_framework import serializers
from ..models.empresa import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class EmpresaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        exclude = ['id']

class EmpresaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        exclude = ['id', 'cpfoucnpj']