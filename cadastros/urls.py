from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.empresa_views import EmpresaViewSet
from .views.usuario_views import UsuarioViewSet
from .views.maquina_views import MaquinaViewSet
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'maquinas', MaquinaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]