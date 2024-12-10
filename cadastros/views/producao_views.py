from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from cadastros.models.producao import Producao
from cadastros.serializers.producao_serializer import ProducaoSerializer
from cadastros.models.usuario import Perfil
from cadastros.utils import CustomPageNumberPagination, ProducaoFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProducaoViewSet(viewsets.ModelViewSet):
    queryset = Producao.objects.all().order_by('-data')
    serializer_class = ProducaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProducaoFilter

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['get'], url_path='ativos')
    def listar_ativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producoes_ativas = Producao.objects.filter(status=True, empresa=empresa_ativa).order_by('-data')

         # Aplicar filtros
        filtered_queryset = ProducaoFilter(request.GET, queryset=producoes_ativas).qs

        # Paginando manualmente
        paginator = CustomPageNumberPagination()
        paginated_query = paginator.paginate_queryset(filtered_queryset, request)

        # Serializar dados paginados
        serializer = ProducaoSerializer(paginated_query, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='inativos')
    def listar_inativos(self, request):
        user = request.user
        perfil = Perfil.objects.get(usuario=user)
        empresa_ativa = perfil.empresaativa

        producoes_inativas = Producao.objects.filter(status=False, empresa=empresa_ativa).order_by('-data')
        
         # Aplicar filtros
        filtered_queryset = ProducaoFilter(request.GET, queryset=producoes_inativas).qs

        # Paginando manualmente
        paginator = CustomPageNumberPagination()
        paginated_query = paginator.paginate_queryset(filtered_queryset, request)

        # Serializar dados paginados
        serializer = ProducaoSerializer(paginated_query, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
