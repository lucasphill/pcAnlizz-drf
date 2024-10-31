from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import User
from apps.accounts.serializers import UserDetailsSerializer, UserRegisterSerializer

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """IsAuthenticated and IsAdmin"""
#     queryset = User.objects.all().order_by('-is_superuser')
#     serializer_class = UserSerializer #need import from apps.accounts.serializer

class UserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    """IsAuthenticated"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)
    
class UserRegisterViewSet(viewsets.ModelViewSet):
    """Anyone"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post',]