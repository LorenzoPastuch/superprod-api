from rest_framework.pagination import PageNumberPagination
import django_filters
from cadastros.models.producao import Producao
from cadastros.serializers.producao_serializer import ProducaoSerializer
from django.db.models import Q
import re



class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Permite a configuração do tamanho da página via URL
    page_size = 25  # Tamanho padrão da página
    max_page_size = 500  # Tamanho máximo da página



class ProducaoFilter(django_filters.FilterSet):

    global_search = django_filters.CharFilter(
        method='filter_global_search', label='Busca Global'
    )

    filter_usuariogravacao = django_filters.CharFilter(
        method='filter_usuariogravacao'
    )

    filter_datagravacao  = django_filters.CharFilter()

    data = django_filters.IsoDateTimeFilter(field_name="data")

    class Meta:
        model = Producao
        fields = {
            'data': ['exact', 'gte', 'lte', 'date'],  # Filtros para data (igual, maior ou igual, menor ou igual)
            'operador__nome': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
            'embalador__nome': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
            'produto__nome': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
            'atributo__nome': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
            'maquina__nome': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
            'maquina__numero': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
            'lote': ['exact', 'icontains', 'exact', 'istartswith', 'iendswith'],  # Igual ou contém
        }
        

    def filter_usuariogravacao(self, queryset, name, value):
        """
        Filtra os registros baseados no valor do campo `usuariogravacao`.
        """
        return queryset.filter(
            Q(logcadastro__usuariogravacao__icontains=value)
        )

    def filter_datagravacao(self, queryset, name, value):
        """
        Filtra os registros baseados no valor do campo `datagravacao`.
        """
        return queryset.filter(
            Q(logcadastro__datagravacao=value)
        )
    
    # def filter_global_search(self, queryset, name, value): #nao possui vantagens de ser usado, muitos problemas envolvidos
    #     """
    #     Filtro global que prioriza resultados mais específicos e expande para buscas mais gerais se necessário.
    #     """
    #     if value:
    #         # Divide o valor em partes (palavras)

    #         # Busca pelo valor completo
    #         filter_conditions_full = Q(
    #             Q(operador__nome__icontains=value) |
    #             Q(embalador__nome__icontains=value) |
    #             Q(produto__nome__icontains=value) |
    #             Q(maquina__nome__icontains=value) |
    #             Q(maquina__numero__icontains=value) |
    #             Q(atributo__nome__icontains=value) |
    #             Q(lote__icontains=value) |
    #             Q(observacao__icontains=value)
    #         )
    #         full_match_results = queryset.filter(filter_conditions_full)

    #         # Se encontrar resultados com o valor completo, retorna
    #         if full_match_results.exists():
    #             return full_match_results
            
    #         search_parts = value.split()

    #         # Busca onde todas as partes estão presentes (AND entre partes)
    #         filter_conditions_all_parts = Q()
    #         for part in search_parts:
    #             filter_conditions_all_parts &= (
    #                 Q(operador__nome__icontains=part) |
    #                 Q(embalador__nome__icontains=part) |
    #                 Q(produto__nome__icontains=part) |
    #                 Q(maquina__nome__icontains=part) |
    #                 Q(maquina__numero__icontains=part) |
    #                 Q(atributo__nome__icontains=part) |
    #                 Q(lote__icontains=part) |
    #                 Q(observacao__icontains=part)
    #             )
    #         all_parts_results = queryset.filter(filter_conditions_all_parts)

    #         # Se encontrar resultados com todas as partes, retorna
    #         if all_parts_results.exists():
    #             return all_parts_results

    #         # # Busca onde qualquer parte está presente (OR entre partes)
    #         filter_conditions_any_part = Q()
    #         for part in search_parts:
    #             filter_conditions_any_part |= (
    #                 Q(operador__nome__icontains=part) |
    #                 Q(embalador__nome__icontains=part) |
    #                 Q(produto__nome__icontains=part) |
    #                 Q(maquina__nome__icontains=part) |
    #                 Q(maquina__numero__icontains=part) |
    #                 Q(atributo__nome__icontains=part) |
    #                 Q(lote__icontains=part) |
    #                 Q(observacao__icontains=part)
    #             )
    #         any_part_results = queryset.filter(filter_conditions_any_part)

    #         # Se encontrar resultados com qualquer parte, retorna
    #         if any_part_results.exists():
    #             return any_part_results

    #     # Retorno vazio se nenhum resultado for encontrado
    #     return queryset.none()