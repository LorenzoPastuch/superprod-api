from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from cadastros.models.maquina import Maquina, MoldeMaquina
from cadastros.models.molde import Molde
from cadastros.serializers.maquina_serializer import MaquinaSerializer

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def register(self, request):
        maquina = request.data.get('maquina')
        moldes = request.data.get('moldes',[])

        maquina = Maquina.objects.create(**maquina)

        for molde in moldes:
            molde_id = molde.get('molde')
            try:
                molde = Molde.objects.get(id=molde_id)
            except Molde.DoesNotExist:
                return Response({'error': f'Molde with id {molde_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            MoldeMaquina.objects.create(
                molde=molde, 
                maquina=maquina
            )

        return Response(status=status.HTTP_201_CREATED)
