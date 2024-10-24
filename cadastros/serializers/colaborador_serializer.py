from rest_framework import serializers
from cadastros.models.colaborador import Colaborador
from cadastros.serializers.empresa_serializer import EmpresaSerializer
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa


class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['id', 'nome', 'funcao', 'numero', 'status']

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        colaborador = Colaborador.objects.create(empresa=empresa_ativa, **validated_data)
        return colaborador
