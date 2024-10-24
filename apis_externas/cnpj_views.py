
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class CnpjViewSet(APIView):
    def get(self, request, cnpj):
        response = requests.get(f'https://www.receitaws.com.br/v1/cnpj/{cnpj}')
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response({"error": "CNPJ não encontrado"}, status=status.HTTP_404_NOT_FOUND)
