from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from cadastros.models.usuario import Perfil

from cadastros.models.molde import Molde
from cadastros.serializers.molde_serializer import MoldeSerializer

class MoldeViewSet(viewsets.ModelViewSet):
    queryset = Molde.objects.all()
    serializer_class = MoldeSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        moldes_ativos = Molde.objects.filter(status=True, empresa=empresa_ativa)
        serializer = MoldeSerializer(moldes_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        moldes_inativos = Molde.objects.filter(status=False, empresa=empresa_ativa)
        serializer = MoldeSerializer(moldes_inativos, many=True, context={'request': request})
        return Response(serializer.data)