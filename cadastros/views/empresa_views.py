from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.empresa import Empresa
from ..serializers.empresa_serializer import EmpresaSerializer
from cadastros.models.usuario import Perfil

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        empresa = serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(EmpresaSerializer(empresa).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(EmpresaSerializer(instance).data)
    
    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        

        empresas_ativos = Empresa.objects.filter(status=True)
        serializer =EmpresaSerializer(empresas_ativos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        
        
        

        empresas_inativos = Empresa.objects.filter(status=False)
        serializer = EmpresaSerializer(empresas_inativos, many=True, context={'request': request})
        return Response(serializer.data)