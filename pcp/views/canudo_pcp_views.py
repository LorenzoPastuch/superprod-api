from rest_framework import viewsets
from rest_framework.decorators import action
from pcp.models.canudo_pcp import CanudoPcp
from rest_framework.response import Response
from cadastros.models.usuario import Perfil
from pcp.serializers.canudo_pcp_serializer import CanudoPcpSerializer


class CanudoPcpViewSet(viewsets.ModelViewSet):
    queryset = CanudoPcp.objects.all()
    serializer_class = CanudoPcpSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producoes_pcp = CanudoPcp.objects.filter(maquina=pk, empresa=empresa_ativa).order_by('ordem')
        serializer = CanudoPcpSerializer(producoes_pcp, many=True, context={'request': request})
        return Response(serializer.data)
    
