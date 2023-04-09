from django.urls import path

from .views import Login, Logout, Refresh, UserListAPIView

#------------------------------------------------------#

urlpatterns = [
    
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('refresh/', Refresh.as_view(), name='refresh'),
    
    path('users/', UserListAPIView.as_view(), name='refresh'),
    
]