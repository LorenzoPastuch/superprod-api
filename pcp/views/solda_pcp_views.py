from rest_framework import viewsets
from rest_framework.decorators import action
from pcp.models.solda_pcp import SoldaPcp
from rest_framework.response import Response
from cadastros.models.usuario import Perfil
from pcp.serializers.solda_pcp_serializer import SoldaPcpSerializer


class SoldaPcpViewSet(viewsets.ModelViewSet):
    queryset = SoldaPcp.objects.all()
    serializer_class = SoldaPcpSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    # @action(detail=False, methods=['get'], url_path='<pk>')
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producoes_pcp = SoldaPcp.objects.filter(maquina=pk, empresa=empresa_ativa).order_by('ordem')
        serializer = SoldaPcpSerializer(producoes_pcp, many=True, context={'request': request})
        return Response(serializer.data)
    
