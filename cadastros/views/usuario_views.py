from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models.usuario import Perfil, UsuarioEmpresa
from ..serializers.usuario_serializer import UsuarioSerializer
from ..models.empresa import Empresa
from django.db import transaction

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        perfil = request.data.get('perfil', {})
        empresas = request.data.get('empresas', [])

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        Perfil.objects.create(status=perfil['status'], empresaativa=perfil['empresaativa'], usuario=user)

        for empresa_data in empresas:
            empresa_id = empresa_data.get('empresa')
            empresapadrao = empresa_data.get('empresapadrao', False)
            
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return Response({'error': f'Empresa with id {empresa_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            UsuarioEmpresa.objects.create(
                usuario=user,
                empresa=empresa,
                empresapadrao=empresapadrao
            )

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ... other viewset methods ...
