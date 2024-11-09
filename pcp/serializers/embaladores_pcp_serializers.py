from rest_framework import serializers
from pcp.models.embaladores_pcp import EmbaladoresPcp

class EmbaladoresPcpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbaladoresPcp
        fields = ['__all__']