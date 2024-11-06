from rest_framework import serializers

class PigmentoSerializer(serializers.Serializer):
    cor = serializers.CharField()
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=3)


class InsumosPcpSerializer(serializers.Serializer):
    pigmentos = PigmentoSerializer(many=True)
    tipo_material = serializers.CharField(source='producao__maquina__produto__material')
    produto = serializers.CharField(source='producao__maquina__produto__nome')
    maquina = serializers.IntegerField(source='producao__maquina__id')
    total_caixas = serializers.IntegerField()
    total_qnt_material = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_embalagens = serializers.IntegerField()

    # class Meta:
    #     model = InsumosPcp
    #     fields = ['total_caixas', 'pigmentos', 'tipo_material', 'total_qnt_material', 'total_embalagem', 'produto', 'maquina']

    # def get_tipo_material(self, obj):

    #     produto=obj.producao.maquina.produto

    #     return produto.material

    # def get_produto(self, obj):

    #     produto = obj.producao.maquina.produto

    #     return produto.nome
    
    
    # # def get_atributo(self, obj):

    # #     atributo = obj.producao.atributo

    # #     return atributo.nome
    
    # def get_maquina(self, obj):

    #     maquina = obj.producao.maquina.maquina

    #     return maquina.numero

    # def get_total_caixas(self, obj):

    #     # total_caixas = InsumosPcp.objects.filter(
    #     #     producao__status__ne='FINALIZADA'
    #     #     ).values(
    #     #         'producao__maquina__id', 
    #     #         'producao__maquina__produto__nome', 
    #     #         'producao__maquina__produto__material'
    #     #     ).annotate(
    #     #         totalcaixas=Sum('caixas')
    #     #     )
    #     return InsumosPcp.objects.filter(producao__maquina=obj.producao.maquina, producao__status__ne='FINALIZADA').aggregate(total=Sum('caixas'))['total']
        # def to_representation(self, instance):

        #     if instance.status == 'FINALIZADA':
        #         return None  


        #     representation = super().to_representation(instance)

        #     producao = instance.producao
        #     maquina = ProducaoPcp.objects.get(producao=producao)

        #     produto = MaquinaPcp.objects.get(maquina=maquina).produto
        #     peso = produto.peso

        #     representation['qnt_material'] = instance.quantidade * peso

        #     return representation
