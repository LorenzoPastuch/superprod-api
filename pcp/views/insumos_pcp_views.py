from rest_framework import viewsets
from rest_framework.decorators import action
from pcp.models.producao_pcp import ProducaoPcp
from pcp.models.insumos_pcp import InsumosPcp
from rest_framework.response import Response
from pcp.serializers.insumos_pcp_serializer import InsumosPcpSerializer, PigmentoSerializer
from django.db.models import Sum


class InsumosPcpViewSet(viewsets.ViewSet):
    def list(self, request):
        # Filtra produções que não estão finalizadas
        producoes = ProducaoPcp.objects.exclude(status='FINALIZADA').values('id')

        # Obtém insumos agrupados por máquina e produto
        insumos = InsumosPcp.objects.filter(
            producao_id__in=producoes
        ).values(
            'producao__maquina__id', 
            'producao__maquina__produto__nome', 
            'producao__maquina__produto__material',
            'producao__maquina__produto__embalagem'
        ).annotate(
            total_caixas=Sum('caixas'),
            total_qnt_material=Sum('qnt_material'),
            total_embalagens=Sum('embalagem')
        )

        resultados = []
        
        # Cria um dicionário para armazenar os resultados por máquina
        maquinas_resultados = {}

        for insumo in insumos:
            maquina_id = insumo['producao__maquina__id']
            
            # Se a máquina não estiver no dicionário, inicializa
            if maquina_id not in maquinas_resultados:
                maquinas_resultados[maquina_id] = {
                    'tipo_material': insumo['producao__maquina__produto__material'],
                    'tipo_embalagem': insumo['producao__maquina__produto__embalagem'],
                    'produto': insumo['producao__maquina__produto__nome'],
                    'maquina': maquina_id,
                    'total_caixas': insumo['total_caixas'],
                    'total_qnt_material': insumo['total_qnt_material'],
                    'total_embalagens': insumo['total_embalagens'],
                    'pigmentos': []
                }

            # Filtra pigmentos para a máquina atual
            pigmentos = InsumosPcp.objects.filter(
                producao__id__in=producoes,
                producao__maquina__id=maquina_id
            ).values(
                'pigmento',
                'producao__atributo__nome'
            )

            pigmentos_serial = [
                PigmentoSerializer({
                    'cor': pigmento['producao__atributo__nome'], 
                    'quantidade': pigmento['pigmento']
                }).data for pigmento in pigmentos
            ]

            # Adiciona pigmentos à lista correspondente da máquina
            maquinas_resultados[maquina_id]['pigmentos'].extend(list(pigmentos_serial))

        # Converte o dicionário em uma lista de resultados
        resultados = list(maquinas_resultados.values())

        return Response(resultados)