from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import serializers

from django.contrib.auth.models import User

#------------------------------------------------------#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class CustomTokenRefreshSerializer(serializers.Serializer):

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        #refresh = self.token_class(attrs["refresh"])
        
        refresh = self.get_token(self.user)
        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:            

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()                 
            #print(refresh.set_jti(), refresh.set_exp(), refresh.set_iat())
            data["refresh"] = str(refresh)
        
        return data


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