from rest_framework import viewsets
from cadastros.models.atributo import Atributo
from cadastros.serializers.atributo_serializer import AtributoSerializer

class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer