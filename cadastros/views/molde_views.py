from rest_framework import viewsets
from cadastros.models.molde import Molde
from cadastros.serializers.molde_serializer import MoldeSerializer

class MoldeViewSet(viewsets.ModelViewSet):
    queryset = Molde.objects.all()
    serializer_class = MoldeSerializer