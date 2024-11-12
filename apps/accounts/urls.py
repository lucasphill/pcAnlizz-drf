from django.urls import path, include

from rest_framework import routers

from apps.accounts.views import  UserDetailsViewSet, UserRegisterViewSet, user_login


app_name = 'Accounts'

router = routers.DefaultRouter()
router.register('register', UserRegisterViewSet, basename='register')
router.register('account', UserDetailsViewSet, basename='details')
#TODO Adicionar rota "account/resetpassword/"

urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_login, name='login'),
]