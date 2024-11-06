from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import User
from apps.accounts.serializers import UserDetailsSerializer, UserRegisterSerializer

from apps.accounts.permissions import NotAuthenticated


class UserDetailsViewSet(viewsets.ModelViewSet):
    """Need authentication. Used to show user info and update."""
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']
    
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)
    
#TODO Add UserForgetPassword

class UserRegisterViewSet(viewsets.ModelViewSet):
    """No need authentication, but not allowed if user is logged. 
    Used to register a new user."""
    
    permission_classes = [NotAuthenticated] #Custom permission class
    
    http_method_names = ['post',]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer