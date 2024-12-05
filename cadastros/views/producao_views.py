from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from cadastros.models.producao import Producao
from cadastros.serializers.producao_serializer import ProducaoSerializer
from cadastros.models.usuario import Perfil

class ProducaoViewSet(viewsets.ModelViewSet):
    queryset = Producao.objects.all().order_by('-data')
    serializer_class = ProducaoSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producoes_ativas = Producao.objects.filter(status=True, empresa=empresa_ativa).order_by('-data')
        serializer = ProducaoSerializer(producoes_ativas, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producoes_inativas = Producao.objects.filter(status=False, empresa=empresa_ativa).order_by('-data')
        serializer = ProducaoSerializer(producoes_inativas, many=True, context={'request': request})
        return Response(serializer.data)