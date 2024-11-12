from rest_framework import viewsets
from rest_framework.decorators import action
from cadastros.models.insumo import Insumo
from cadastros.serializers.insumo_serializer import InsumoSerializer
from cadastros.models.usuario import Perfil
from rest_framework.response import Response

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        insumos_ativos = Insumo.objects.filter(status=True, empresa=empresa_ativa)
        serializer = InsumoSerializer(insumos_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        insumos_inativos = Insumo.objects.filter(status=False, empresa=empresa_ativa)
        serializer = InsumoSerializer(insumos_inativos, many=True, context={'request': request})
        return Response(serializer.data)
