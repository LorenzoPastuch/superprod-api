from rest_framework import viewsets
from cadastros.models.atributo import Atributo
from rest_framework.decorators import action
from rest_framework.response import Response
from cadastros.serializers.atributo_serializer import AtributoSerializer
from cadastros.models.usuario import Perfil

class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer

    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        atributos_ativos = Atributo.objects.filter(status=True, empresa=empresa_ativa)
        serializer = AtributoSerializer(atributos_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        atributos_inativos = Atributo.objects.filter(status=False, empresa=empresa_ativa)
        serializer = AtributoSerializer(atributos_inativos, many=True, context={'request': request})
        return Response(serializer.data)