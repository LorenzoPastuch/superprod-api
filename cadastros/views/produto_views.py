from rest_framework import viewsets
from rest_framework.decorators import action
from cadastros.models.produto import Produto
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.models.usuario import Perfil
from rest_framework.response import Response

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        produtos_ativos = Produto.objects.filter(status=True, empresa=empresa_ativa)
        serializer = ProdutoSerializer(produtos_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        produtos_inativos = Produto.objects.filter(status=False, empresa=empresa_ativa)
        serializer = ProdutoSerializer(produtos_inativos, many=True, context={'request': request})
        return Response(serializer.data)
