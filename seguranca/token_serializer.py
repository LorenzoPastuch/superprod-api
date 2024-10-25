from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user ):
        token = super().get_token(user)

        token['exp'] = token['exp']
        token['user_name'] = user.username
        token['authorities'] = [perm.codename for perm in user.user_permissions.all()]
        token['jti'] = token['jti']
        token['scope'] = ["read", "write"]
             
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Adiciona os campos customizados à resposta
        data['access_token'] = data.pop('access')
        data['token_type'] = 'bearer'
        data['expires_in'] = 604799  # 7 dias em segundos
        data['jti'] = self.get_token(self.user)['jti']
        data['scope'] = "read write"

        return data