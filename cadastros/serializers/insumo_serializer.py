from rest_framework import serializers
from cadastros.models.insumo import Insumo
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.log_cadastro import Log_cadastro
from cadastros.serializers.log_cadastro_serializer import LogCadastroMixin

class InsumoSerializer(LogCadastroMixin, serializers.ModelSerializer):
    usuariogravacao = serializers.SerializerMethodField()
    datagravacao = serializers.SerializerMethodField()
    class Meta:
        model = Insumo
        fields = ['id', 'nome', 'codigo', 'classe', 'codigowms', 'status', 'usuariogravacao', 'datagravacao']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        insumo = Insumo.objects.create(empresa=empresa_ativa, **validated_data)

        self.registrar_log(
            comando=f"Criar insumo de ID {insumo.id}",
            usuario=user,
            instance=insumo,
        )
        return insumo
    
    def get_usuariogravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(insumo=obj).order_by('-datagravacao').first()
        if log:
            return log.usuariogravacao
        return None

    def get_datagravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(insumo=obj).order_by('-datagravacao').first()
        if log:
            return log.datagravacao
        return None

