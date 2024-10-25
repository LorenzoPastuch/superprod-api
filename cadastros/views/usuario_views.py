from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models.usuario import Perfil, UsuarioEmpresa
from ..serializers.usuario_serializer import UsuarioCreateSerializer, UsuarioListSerializer
from ..models.empresa import Empresa
from django.contrib.auth.models import Permission

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioCreateSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UsuarioListSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        status_user = request.data.get('status')
        empresaativa = request.data.get('empresaativa')
        empresapadrao = request.data.get('empresapadrao')
        empresas = request.data.get('empresas', [])
        permissoes = request.data.get('permissoes',[])

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        Perfil.objects.create(status=status_user, empresaativa=empresaativa, usuario=user)

        for empresa_data in empresas:
            empresa_id = empresa_data.get('id')
            
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return Response({'error': f'Empresa with id {empresa_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            UsuarioEmpresa.objects.create(
                usuario=user,
                empresa=empresa,
                empresapadrao=empresapadrao
            )

        for permissao in permissoes:
            codename = permissao.get('codename')
            try:
                permissao = Permission.objects.get(codename=codename)
                user.user_permissions.add(permissao)
            except Permission.DoesNotExist:
                return Response({'error': 'One or more permissions do not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        try:
           user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        status_user = request.data.get('status')
        empresaativa = request.data.get('empresaativa')
        empresapadrao = request.data.get('empresapadrao')
        empresas = request.data.get('empresas', [])
        permissoes = request.data.get('permissoes',[])


        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        perfil = user.perfil
        perfil.status = status_user
        perfil.empresaativa = empresaativa
        perfil.save()

        user.usuarioempresa_set.all().delete()  # Remove as empresas existentes
        for empresa_data in empresas:
            empresa_id = empresa_data.get('id')
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return Response({'error': f'Empresa with id {empresa_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            UsuarioEmpresa.objects.create(
                usuario=user,
                empresa=empresa,
                empresapadrao=empresapadrao
            )

        # Atualiza as permissões do usuário
        user.user_permissions.clear()  # Limpa permissões existentes
        for permissao in permissoes:
            codename = permissao.get('codename')
            try:
                permissao = Permission.objects.get(codename=codename)
                print(permissao)
                user.user_permissions.add(permissao)
            except Permission.DoesNotExist:
                return Response({'error': 'One or more permissions do not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    @action(detail=True, methods=['put'], url_path='atualizar-empresa-ativa')
    def empresaativa(self, request, pk=None):
        try:
            usuario = self.get_object()
            nova_empresa_id = request.data.get('empresaativa')
            print(nova_empresa_id)

            if not nova_empresa_id:
                return Response({'error': 'ID da empresa é necessário.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica se a empresa existe e se está associada ao usuário
            empresa_usuario = UsuarioEmpresa.objects.filter(usuario=usuario, empresa_id=nova_empresa_id).first()
            if not empresa_usuario:
                return Response({'error': 'Empresa não encontrada ou não associada a este usuário.'}, status=status.HTTP_404_NOT_FOUND)

            perfil = usuario.perfil
            print(perfil)

            # Atualiza a empresa ativa do usuário
            perfil.empresaativa = nova_empresa_id
            perfil.save()

            return Response({'success': 'Empresa ativa atualizada com sucesso.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['put'], url_path='reset')
    def reset_senha(self, request, pk=None):
        try:
           user = self.get_object()
           user.set_password('123456')
           user.save()
           return Response({'success': 'Senha resetada com sucesso.'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'], url_path='alterar-senha')
    def alterar_senha(self, request, pk=None):
        nova_senha = request.data.get('nova_senha')
        user = self.get_object()
        user.set_password(nova_senha)
        user.save()
        return Response({'success': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)
        


    


    
    
        
