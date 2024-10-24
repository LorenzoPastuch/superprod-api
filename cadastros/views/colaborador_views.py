from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from cadastros.models.colaborador import Colaborador
from cadastros.serializers.colaborador_serializer import ColaboradorSerializer
from cadastros.models.usuario import Perfil

class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        colaboradores_ativos = Colaborador.objects.filter(status=True, empresa=empresa_ativa)
        serializer = ColaboradorSerializer(colaboradores_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        colaboradores_inativos = Colaborador.objects.filter(status=False, empresa=empresa_ativa)
        serializer = ColaboradorSerializer(colaboradores_inativos, many=True, context={'request': request})
        return Response(serializer.data)
