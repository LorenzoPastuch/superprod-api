from rest_framework import serializers
from django.utils import timezone
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from almoxarifado.models.registro_almoxarifado import RegistroAlmoxarifado
from cadastros.models.insumo import Insumo
from cadastros.serializers.insumo_serializer import InsumoSerializer

class RegistroAlmoxarifadoSerializer(serializers.ModelSerializer):
    insumo = serializers.SerializerMethodField()
    nome = serializers.SerializerMethodField()
    classe = serializers.SerializerMethodField()
    codigowms = serializers.SerializerMethodField()

    class Meta:
        model = RegistroAlmoxarifado
        fields = ['id', 'insumo', 'nome', 'classe','quantidade', 'tipo_movimentacao', 'codigowms', 'statuswms', 'datagravacao', 'usuariogravacao']
        ready_only_fields = ['usuariogravacao']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        insumo = self.context['request'].data.get('insumo', {})
        quantidade = self.context['request'].data.get('quantidade')
        tipo_movimentacao = self.context['request'].data.get('tipo_movimentacao')
        statuswms = self.context['request'].data.get('statuswms')

        registro = RegistroAlmoxarifado.objects.create(
            empresa=empresa_ativa,
            insumo = Insumo.objects.get(id=insumo['id']),
            quantidade = quantidade,
            statuswms = statuswms if statuswms else False,
            tipo_movimentacao = tipo_movimentacao,
            usuariogravacao=user.username,
            datagravacao=timezone.now()
        )
        return registro
    
    def get_insumo(self, obj):
        return InsumoSerializer(obj.insumo).data
    
    def get_nome(self, obj):
        return obj.insumo.nome

    def get_classe(self, obj):
        return obj.insumo.classe
    
    def get_codigowms(self, obj):
        return obj.insumo.codigowms

