
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken, AccessToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenBlacklistView, 
    TokenRefreshView
)


from rest_framework.generics import (ListAPIView) 

from .serializers import CustomTokenObtainPairSerializer, UserSerializer, CustomTokenRefreshSerializer, WhiteListTokenDeviceSerializer
from .models import WhiteListTokenDevice
#------------------------------------------------------#

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):        
        # for key,value in request.META.items():
        #     print({key:value})
        
        username = request.data.get('username')
        password = request.data.get('password')        
        user = authenticate(
            username=username,
            password=password
        )        
        if user:
            #validando si existe algun refresh libre antes de iniciar sesion
            outstanding_tokens = OutstandingToken.objects.filter(user=user)        
            outstanding_not_blacklisted = []
            
            for value in outstanding_tokens:                
                check = BlacklistedToken.objects.filter(token=value)
                if not check.exists():
                    outstanding_not_blacklisted.append(value)               
                
            if outstanding_not_blacklisted:
                for token in outstanding_not_blacklisted:
                    BlacklistedToken.objects.create(token=token)
                    print("/////////////////////////////")            
                        
            serializer = self.get_serializer(data=request.data)
            
            if serializer.is_valid():
                instance = OutstandingToken.objects.get(token=serializer.validated_data['refresh'])
                
                #asociando el ip y browser al refresh
                WhiteListTokenDevice.objects.create(
                    ip = request.META.get('REMOTE_ADDR'),
                    browser = request.META.get('HTTP_USER_AGENT'),
                    token=instance.id
                )
                
                # ip = request.META.get('REMOTE_ADDR')
                # browser = request.META.get('HTTP_USER_AGENT')
                
                # whitelist_serializer = WhiteListTokenDeviceSerializer(data={
                #     'ip':ip,
                #     'browser':browser,
                #     'token':instance.id
                # })
                # if whitelist_serializer.is_valid():
                #     whitelist_serializer.save()
                
                user_serializer = UserSerializer(user)                
                return Response({
                    'AccessToken':serializer.validated_data['access'],
                    'RefreshToken':serializer.validated_data['refresh'],
                    'User':user_serializer.data,
                    'Message':'Inicio de sesion exitoso',
                    #'headers':headers,
                }, status=status.HTTP_200_OK)
               
        return Response({
            'error':'Usuario o Password incorrectos',
            }, status=status.HTTP_400_BAD_REQUEST)
        

        
        



class Logout(TokenBlacklistView):
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        return Response({
            'message':'Token eliminado',
            #'data':serializer.validated_data
            }, status=status.HTTP_200_OK)




class Refresh(TokenRefreshView):    
    serializer_class = CustomTokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        
        #validando si el ip y browser de la peticion es el permitido
        actual_ip = request.META.get('REMOTE_ADDR')
        actual_browser = request.META.get('HTTP_USER_AGENT')                
        token = request.data.get('refresh')
        instance = OutstandingToken.objects.get(token=token)
        # instance_device = WhiteListTokenDevice.objects.get(token=instance.id)
        
        device = WhiteListTokenDevice.objects.get(
            ip=actual_ip,
            browser=actual_browser,
            token=instance.id
            )        
                
        # if actual_ip == instance_device.ip and actual_browser == instance_device.browser:
        if device:
        
            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)          

                # instance = OutstandingToken.objects.get(token=serializer.validated_data['refresh'])

                # whitelist_serializer = WhiteListTokenDeviceSerializer(data={
                #     'ip':actual_ip,
                #     'browser':actual_browser,
                #     'token':instance.id
                # })
                # if whitelist_serializer.is_valid():
                #     whitelist_serializer.save()

            except TokenError as e:
                raise InvalidToken(e.args[0])     

            return Response({
                'AccessToken':serializer.validated_data['access'],
                'RefreshToken':serializer.validated_data['refresh'],
                }, status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_401_UNAUTHORIZED)