from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from pcp.serializers.embaladores_pcp_serializers import EmbaladoresPcpSerializer
from pcp.models.embaladores_pcp import EmbaladoresPcp

class EmbaladoresPcpViewSet(viewsets.ModelViewSet):
    queryset = EmbaladoresPcp.objects.all()
    serializer_class = EmbaladoresPcpSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['get'], url_path='rotacionar')
    def rotacionar_embaladores(self, request):
        try:
            # Filtrar máquinas ligadas no setor 'INJETORA'
            maquinas_ligadas = EmbaladoresPcp.objects.filter(Q(maquina__status='EM PRODUÇÃO') | Q(maquina__status='FILA DE PRODUÇÃO'), Q(setor='INJETORA') | Q(setor='EXTRUSORA')).order_by('maquina')
            # Verificar se há máquinas ligadas disponíveis
            if not maquinas_ligadas.exists():
                return Response({"message": "Nenhuma máquina ligada no setor 'injetora' para rotação."}, status=status.HTTP_200_OK)

            # Filtrar embaladores associados ao setor 'INJETORA'
            embaladores_injetora = list(EmbaladoresPcp.objects.filter(Q(maquina__status='EM PRODUÇÃO') | Q(maquina__status='FILA DE PRODUÇÃO'), Q(setor='INJETORA') | Q(setor='EXTRUSORA')))
            # Verificar se há embaladores disponíveis
            if not embaladores_injetora:
                return Response({"message": "Nenhum embalador disponível no setor 'injetora'."}, status=status.HTTP_200_OK)
            
            total_embaladores = len(embaladores_injetora)
            total_maquinas = len(maquinas_ligadas)
            print(total_embaladores)
            print(total_maquinas)

            # Verificar se as listas de embaladores e máquinas têm o mesmo tamanho
            # Rotacionar os embaladores do setor 'INJETORA' nas máquinas ligadas
            total_embaladores = len(embaladores_injetora)
            for index, maquina in enumerate(maquinas_ligadas):
                embalador_pcp = embaladores_injetora[(index -1) % total_embaladores] 
                colaborador = embalador_pcp.embalador  # Obter a instância de Colaborador
                maquina.embalador = colaborador 
                maquina.save()

            return Response({"message": "Embaladores rotacionados com sucesso nas máquinas ligadas."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
