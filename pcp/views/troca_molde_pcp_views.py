from rest_framework import viewsets
from rest_framework.decorators import action
from pcp.models.troca_molde_pcp import TrocaMoldePcp
from rest_framework.response import Response
from cadastros.models.usuario import Perfil
from pcp.serializers.troca_molde_pcp_serializer import TrocaMoldePcpSerializer
from cadastros.serializers.produto_serializer import ProdutoSerializer


class TrocaMoldePcpViewSet(viewsets.ModelViewSet):
    queryset = TrocaMoldePcp.objects.all()
    serializer_class = TrocaMoldePcpSerializer

    def get_serializer_context(self):
        return {'request': self.request}