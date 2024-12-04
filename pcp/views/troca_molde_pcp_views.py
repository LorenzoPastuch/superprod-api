from rest_framework import viewsets
from pcp.models.troca_molde_pcp import TrocaMoldePcp
from pcp.serializers.troca_molde_pcp_serializer import TrocaMoldePcpSerializer


class TrocaMoldePcpViewSet(viewsets.ModelViewSet):
    queryset = TrocaMoldePcp.objects.all().order_by('ordem')
    serializer_class = TrocaMoldePcpSerializer

    def get_serializer_context(self):
        return {'request': self.request}