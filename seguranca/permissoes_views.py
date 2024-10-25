# super_prod_api/seguranca/views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get(self, request, id_user):
        try:
            # Obter o usuário pelo ID
            user = User.objects.get(id=id_user)
            # Obter as permissões do usuário
            permissions = [perm.codename for perm in user.user_permissions.all()]

            return Response({'user_id': user.id, 'permissions': permissions}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)