from rest_framework import serializers
from cadastros.models.atributo import Atributo
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.serializers.empresa_serializer import EmpresaSerializer

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = ['id', 'nome', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        atributo = Atributo.objects.create(empresa=empresa_ativa, **validated_data)
        return atributo