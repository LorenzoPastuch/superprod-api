from rest_framework import viewsets
from cadastros.models.colaborador import Colaborador
from cadastros.serializers.colaborador_serializer import ColaboradorSerializer

class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer