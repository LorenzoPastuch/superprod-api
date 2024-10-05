from rest_framework import viewsets
from cadastros.models.producao import Producao
from cadastros.serializers.producao_serializer import ProducaoSerializer

class ProducaoViewSet(viewsets.ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer