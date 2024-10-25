from rest_framework import serializers
from cadastros.models.atributo import Atributo
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.log_cadastro import Log_cadastro
from cadastros.serializers.log_cadastro_serializer import LogCadastroMixin

class AtributoSerializer(LogCadastroMixin, serializers.ModelSerializer):
    usuariogravacao = serializers.SerializerMethodField()
    datagravacao = serializers.SerializerMethodField()
    class Meta:
        model = Atributo
        fields = ['id', 'nome', 'status', 'usuariogravacao', 'datagravacao']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        atributo = Atributo.objects.create(empresa=empresa_ativa, **validated_data)

        self.registrar_log(
            comando=f"Criar Atributo de ID {atributo.id}",
            usuario=user,
            instance=atributo,
        )
        return atributo
    
    def get_usuariogravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(atributo=obj).order_by('-datagravacao').first()
        if log:
            return log.usuariogravacao
        return None

    def get_datagravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(atributo=obj).order_by('-datagravacao').first()
        if log:
            return log.datagravacao
        return None