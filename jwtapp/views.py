
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSlidingSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenBlacklistView, 
    TokenRefreshView
)


from rest_framework.generics import (ListAPIView) 

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
#------------------------------------------------------#

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        #username = request.data.get('username')
        #password = request.data.get('password')
        
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        return Response({
            'AccessToken':serializer.validated_data['access'],
            'RefreshToken':serializer.validated_data['refresh'],
        }, status=status.HTTP_200_OK)
        
        # user = authenticate(
        #     username=username,
        #     password=password
        # )
        
        # if user:
        #     sserializer = self.get_serializer(data=request.data)
            
        #     if login_serializer.is_valid():                
        #         user_serializer = UserJWTAuthSerializer(user)                
        #         return Response({
        #             'AccessToken':serializer.validated_data['access'],
        #             'RefreshToken':serializer.validated_data['refresh'],
        #             'User':user_serializer.data,
        #             'Message':'Inicio de sesion exitoso',
        #             'status': status.HTTP_200_OK
        #         }, status=status.HTTP_200_OK)
        #     return Response({
        #         'error':'Usuario o Password incorrectos',
        #         'status':status.HTTP_400_BAD_REQUEST
        #         }, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({
        #     'error':'Usuario o Password incorrectos',
        #     'status':status.HTTP_400_BAD_REQUEST
        #     }, status=status.HTTP_400_BAD_REQUEST)
        

        
        



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
    #serializer_class = TokenRefreshSlidingSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        return Response({
            'AccessToken':serializer.validated_data['access'],
            'RefreshToken':serializer.validated_data['refresh'],
            }, status=status.HTTP_200_OK)