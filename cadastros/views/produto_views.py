from rest_framework import viewsets
from cadastros.models.produto import Produto
from cadastros.serializers.produto_serializer import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
