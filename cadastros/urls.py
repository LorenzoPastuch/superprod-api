from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.empresa_views import EmpresaViewSet
from .views.usuario_views import UsuarioViewSet
from .views.maquina_views import MaquinaViewSet
from .views.produto_views import ProdutoViewSet
from .views.molde_views import MoldeViewSet
from .views.colaborador_views import ColaboradorViewSet
from .views.producao_views import ProducaoViewSet
from .views.atributo_views import AtributoViewSet
from .views.insumo_views import InsumoViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'empresas', EmpresaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'moldes', MoldeViewSet)
router.register(r'colaboradores', ColaboradorViewSet)
router.register(r'atributos', AtributoViewSet)
router.register(r'producoes', ProducaoViewSet)
router.register(r'insumos', InsumoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]