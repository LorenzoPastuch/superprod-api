from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models.usuario import Perfil, UsuarioEmpresa
from ..serializers.usuario_serializer import PermissoesSerializer, UsuarioCreateSerializer, UsuarioListSerializer
from ..models.empresa import Empresa
from django.contrib.auth.models import Permission
from django.db import transaction

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

    # @action(detail=False, methods=['get'], url_path='empresas/ativa')
    # def empresas_ativas(self, request):
    #     user = request.user
    #     perfil = Perfil.objects.filter(usuario=user).first()
        
    #     if perfil and perfil.empresaativa:
    #         return Response({'empresaativa': perfil.empresaativa}, status=status.HTTP_200_OK)
        
    #     return Response({'error': 'No active company found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='permissoes')
    def permissoes(self, request):
        permissoes = Permission.objects.all()
        serializer = PermissoesSerializer(permissoes, many=True)
        
        return Response(serializer.data)
    
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


    # def retrieve(self, request, pk=None):
    #     user = self.get_object()
    #     perfil = Perfil.objects.filter(usuario=user).first()
    #     empresa = Empresa.objects.filter(id=perfil.empresaativa).first()
    #     permissoes = user.get_all_permissions()
    #     permissoes_formatadas = []

    #     for perm in permissoes:
    #         codename = perm.split('.')
    #         permission_obj = Permission.objects.get(codename=codename[1])  # Obtém o objeto Permission
    #         permissoes_formatadas.append({
    #             "id": permission_obj.id,  # Usa o ID real da permissão
    #             "descricao": permission_obj.codename  # Usa o nome da permissão como descrição
    #         })

    #     response_data = {
    #         "id": user.id,
    #         "status": perfil.status if perfil else None,
    #         "nome": f"{user.first_name} {user.last_name}",
    #         "login": user.username,
    #         "empresaativa": empresa.razaosocial,
    #         "idEmpresaativa": perfil.empresaativa,
    #         "permissoes": list(permissoes_formatadas)
    #     }

    #     return Response(response_data, status=status.HTTP_200_OK)
    
    
        
