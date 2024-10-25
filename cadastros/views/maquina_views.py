from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from cadastros.models.maquina import Maquina, MoldeMaquina
from cadastros.models.molde import Molde
from cadastros.serializers.maquina_serializer import MaquinaSerializer
from cadastros.models.usuario import Perfil

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        maquinas_ativos = Maquina.objects.filter(status=True, empresa=empresa_ativa)
        serializer =MaquinaSerializer(maquinas_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        maquinas_inativos = Maquina.objects.filter(status=False, empresa=empresa_ativa)
        serializer = MaquinaSerializer(maquinas_inativos, many=True, context={'request': request})
        return Response(serializer.data)