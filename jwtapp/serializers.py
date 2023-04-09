from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers

from django.contrib.auth.models import User

#------------------------------------------------------#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass



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