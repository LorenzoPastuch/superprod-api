from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from ..models.usuario import Perfil, UsuarioEmpresa
from ..models.empresa import Empresa

class UsuarioEmpresaSerializer(serializers.ModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    
    class Meta:
        model = UsuarioEmpresa
        fields = ['empresa', 'empresapadrao']

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['status', 'empresaativa']

class UsuarioSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer()
    empresas = UsuarioEmpresaSerializer(source='usuarioempresa_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil','password', 'empresas']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        perfil_data = validated_data.pop('perfil', {})
        empresas_data = validated_data.pop('usuarioempresa_set', [])
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        Perfil.objects.create(usuario=user, **perfil_data)

        for empresa_data in empresas_data:
            UsuarioEmpresa.objects.create(usuario=user, **empresa_data)

        return user