from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.registro_almoxarifado_views import RegistrosAlmoxarifadoViewset

router = DefaultRouter(trailing_slash=False)
router.register(r'registros', RegistrosAlmoxarifadoViewset)

urlpatterns = [
    path('', include(router.urls)),
]