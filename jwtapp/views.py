
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenBlacklistView, 
    TokenRefreshView
)


from rest_framework.generics import (ListAPIView) 

from .serializers import CustomTokenObtainPairSerializer, UserSerializer, CustomTokenRefreshSerializer
#------------------------------------------------------#

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # return Response({
        #     'AccessToken':serializer.validated_data['access'],
        #     'RefreshToken':serializer.validated_data['refresh'],
        # }, status=status.HTTP_200_OK)
        
        user = authenticate(
            username=username,
            password=password
        )
        
        if user:
            outstanding_tokens = OutstandingToken.objects.filter(user=user)
            
            # in_outstanding = outstanding_tokens.count()            
            # outstanding_blacklisted = []            
            if outstanding_tokens.exists():
                outstanding_not_blacklisted = []
                
                for value in outstanding_tokens:
                    # print(value)
                    check = BlacklistedToken.objects.filter(token=value)

                    if not check.exists():
                        outstanding_not_blacklisted.append(value)

                    # if check.exists():
                    #     outstanding_blacklisted.append(check.values('token'))
                    # else:
                    #     outstanding_not_blacklisted.append(value)

                for token in outstanding_not_blacklisted:
                    BlacklistedToken.objects.create(token=token)
                    print("/////////////////////////////")
                
                
            # print(in_outstanding)
            # print(outstanding_blacklisted)
            # print(outstanding_not_blacklisted)
                        
            serializer = self.get_serializer(data=request.data)
            
            if serializer.is_valid():                
                user_serializer = UserSerializer(user)                
                return Response({
                    'AccessToken':serializer.validated_data['access'],
                    'RefreshToken':serializer.validated_data['refresh'],
                    'User':user_serializer.data,
                    'Message':'Inicio de sesion exitoso',
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
    #serializer_class = TokenObtainPairSerializer
    serializer_class = CustomTokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        
        refreshtoken = request.data.get('refresh')
        
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        try:            
            refreshtoken = RefreshToken(refreshtoken)

            user = refreshtoken.payload['user_id']        
            user = User.objects.get(id=user)

            outstanding_tokens = OutstandingToken.objects.filter(user=user)
            #actual_refresh = OutstandingToken.objects.filter(token=request.data.get('refresh')).values('token')
            # print(actual_refresh)
            outstanding_not_blacklisted = []

            for value in outstanding_tokens:

                check = BlacklistedToken.objects.filter(token=value)

                if not check.exists():
                    
                    outstanding_not_blacklisted.append(value)        

            #outstanding_not_blacklisted.remove(actual_refresh)
            #print(outstanding_not_blacklisted)
            for token in outstanding_not_blacklisted:
                BlacklistedToken.objects.create(token=token)
                print("/////////////////////////////")
            
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        
               
        return Response({
            'AccessToken':serializer.validated_data['access'],
            'RefreshToken':serializer.validated_data['refresh'],
            }, status=status.HTTP_200_OK)