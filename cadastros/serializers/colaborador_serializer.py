from rest_framework import serializers
from cadastros.models.colaborador import Colaborador
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.log_cadastro import Log_cadastro
from cadastros.serializers.log_cadastro_serializer import LogCadastroMixin


class ColaboradorSerializer(LogCadastroMixin, serializers.ModelSerializer):
    usuariogravacao = serializers.SerializerMethodField()
    datagravacao = serializers.SerializerMethodField()
    class Meta:
        model = Colaborador
        fields = ['id', 'nome', 'funcao', 'numero', 'status', 'usuariogravacao', 'datagravacao']

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        colaborador = Colaborador.objects.create(empresa=empresa_ativa, **validated_data)

        self.registrar_log(
            comando=f"Criar Colaborador de ID {colaborador.id}",
            usuario=user,
            instance=colaborador,
        )
        return colaborador

    def get_usuariogravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(colaborador=obj).order_by('-datagravacao').first()
        if log:
            return log.usuariogravacao
        return None

    def get_datagravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(colaborador=obj).order_by('-datagravacao').first()
        if log:
            return log.datagravacao
        return None