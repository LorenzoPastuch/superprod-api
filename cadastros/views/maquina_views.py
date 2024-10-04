from rest_framework import viewsets
from cadastros.models.maquina import Maquina
from cadastros.serializers.maquina_serializer import MaquinaSerializer

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
