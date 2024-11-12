from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from apps.accounts.models import User
from apps.accounts.serializers import UserDetailsSerializer, UserRegisterSerializer
from apps.accounts.permissions import NotAuthenticated

#TODO Adicionar comentários nas funções e refatorar o codigo
class UserDetailsViewSet(viewsets.ModelViewSet):
    """Need authentication. Used to show user info and update."""
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']
    
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)
    

class UserRegisterViewSet(viewsets.ModelViewSet):
    """No need authentication, but not allowed if user is logged. 
    Used to register a new user."""
    #TODO revizar o erro de acessar essa rota mesmo com login
    permission_classes = [NotAuthenticated] #Custom permission class
    
    http_method_names = ['post',]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)