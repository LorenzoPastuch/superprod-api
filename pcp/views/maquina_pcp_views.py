from rest_framework import viewsets
from rest_framework.decorators import action
from pcp.models.maquina_pcp import MaquinaPcp
from rest_framework.response import Response
from cadastros.models.usuario import Perfil
from pcp.serializers.maquina_pcp_serializer import MaquinaPcpSerializer
from cadastros.serializers.produto_serializer import ProdutoSerializer


class MaquinaPcpViewSet(viewsets.ModelViewSet):
    queryset = MaquinaPcp.objects.all().order_by('maquina__nome', 'maquina__numero')
    serializer_class = MaquinaPcpSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=True, methods=['get'], url_path='produto')
    def get_produto(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producao_pcp = MaquinaPcp.objects.filter(maquina=pk, empresa=empresa_ativa).first()
        produto_serializer = ProdutoSerializer(producao_pcp.produto, context={'request': request})
        return Response(produto_serializer.data)