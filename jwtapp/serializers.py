from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import datetime_from_epoch

from rest_framework import serializers

from django.contrib.auth.models import User

from .models import WhiteListTokenDevice
#------------------------------------------------------------------------#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


#------------------------------------------------------------------------#
class CustomTokenRefreshSerializer(serializers.Serializer):
    
    # Definiendo los campos del serializador
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        #obteniendo el nuevo refresh a partir de la instancia del refresh anterior para sacar su access
        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}

        #si ROTATE_REFRESH_TOKENS es true devolvemos un nuevo refresh token
        if api_settings.ROTATE_REFRESH_TOKENS:
            #si BLACKLIST_AFTER_ROTATION es true se añade el refresh recibido a la blacklist
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()                
            data["refresh"] = str(refresh)
            
            #guardando el nuevo refresh token a la lista de tokens pendientes
            outstanding_token = OutstandingToken(
                token=str(refresh),
                created_at=refresh.current_time,
                expires_at=datetime_from_epoch(refresh.get('exp')),
                user_id=refresh.get('user_id'),
                jti=refresh.get('jti')
            )
            outstanding_token.save()
            
        #print(refresh.current_time)
        return data




#------------------------------------------------------------------------#
class WhiteListTokenDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhiteListTokenDevice
        fields = [
            'id',
            'ip',
            'browser',
            'token',
        ]

#------------------------------------------------------------------------#
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            ]