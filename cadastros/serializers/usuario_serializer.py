from rest_framework import serializers
from django.contrib.auth.models import User, Permission

from ..serializers.empresa_serializer import EmpresaSerializer
from ..models.usuario import Perfil, UsuarioEmpresa

class UsuarioListSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    empresaativa = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nome', 'empresaativa', 'status']

    def get_nome(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_empresaativa(self, obj):
        return obj.perfil.empresaativa

    def get_status(self, obj):
        return obj.perfil.status
    
class UsuarioEmpresaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()

    class Meta:
        model = UsuarioEmpresa
        fields = ['empresa', 'empresapadrao']

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['status', 'empresaativa']

class PermissoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id','codename']

class UsuarioCreateSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    empresaativa = serializers.SerializerMethodField()
    empresas = serializers.SerializerMethodField()
    permissoes = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','password', 'status', 'empresaativa', 'empresas', 'permissoes']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        status = validated_data.pop('status')
        empresaativa = validated_data.pop('empresaativa')
        empresapadrao = validated_data.pop('empresapadrao')
        empresas_data = validated_data.pop('usuarioempresa_set', [])
        permissoes_data = validated_data.pop('permissoes', [])
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        perfil = Perfil.objects.create(usuario=user)
        perfil.status = status
        perfil.empresaativa = empresaativa
        perfil.save()

        for empresa_data in empresas_data:
            UsuarioEmpresa.objects.create(usuario=user, empresa=empresapadrao, **empresa_data)

        if permissoes_data:
            codenames = [permissao['codename'] for permissao in permissoes_data]
            permissions = Permission.objects.filter(codename__in=codenames)
            user.user_permissions.set(permissions)

        return user
    
    def get_permissoes(self, obj):
        permissoes = obj.user_permissions.all()
        return PermissoesSerializer(permissoes, many=True).data
    
    def get_status(self, obj):
        return obj.perfil.status
    
    def get_empresaativa(self, obj):
        return obj.perfil.empresaativa
    
    def get_empresas(self, obj):
        empresas = obj.usuarioempresa_set.all()
        return EmpresaSerializer([ue.empresa for ue in empresas], many=True).data