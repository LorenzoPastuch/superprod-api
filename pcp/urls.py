from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pcp.views.producao_pcp_views import ProducaoPcpViewSet
from pcp.views.maquina_pcp_views import MaquinaPcpViewSet
from pcp.views.insumos_pcp_views import InsumosPcpViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'producao', ProducaoPcpViewSet)
router.register(r'controle', MaquinaPcpViewSet)
router.register(r'insumos', InsumosPcpViewSet, basename='InsumosPcp')

urlpatterns = [
    path('', include(router.urls)),
    
]