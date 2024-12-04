from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from almoxarifado.models.registro_almoxarifado import RegistroAlmoxarifado
from almoxarifado.serializers.registro_almoxarifado_serializer import RegistroAlmoxarifadoSerializer
from cadastros.models.usuario import Perfil

class RegistrosAlmoxarifadoViewset(viewsets.ModelViewSet):
    queryset = RegistroAlmoxarifado.objects.all().order_by('-datagravacao')
    serializer_class = RegistroAlmoxarifadoSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['get'], url_path='exportados')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        registros_exportados = RegistroAlmoxarifado.objects.filter(statuswms=True, empresa=empresa_ativa).order_by('-datagravacao')
        serializer = RegistroAlmoxarifadoSerializer(registros_exportados, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='naoexportados')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        registros_nao_exportados = RegistroAlmoxarifado.objects.filter(statuswms=False, empresa=empresa_ativa).order_by('-datagravacao')
        serializer = RegistroAlmoxarifadoSerializer(registros_nao_exportados, many=True, context={'request': request})
        return Response(serializer.data)