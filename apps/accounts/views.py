from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import User
from apps.accounts.serializers import UserDetailsSerializer, UserRegisterSerializer


class UserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    """IsAuthenticated. Used to see informations of logged user."""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)

class UserRegisterViewSet(viewsets.ModelViewSet):
    """Anyone. Used to create a new user in the system 
    1 - add validation 'if logged' 
    2 - add validation for password"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post',]