from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pcp.views.producao_pcp_views import ProducaoPcpViewSet
from pcp.views.maquina_pcp_views import MaquinaPcpViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'producao', ProducaoPcpViewSet)
router.register(r'controle', MaquinaPcpViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]