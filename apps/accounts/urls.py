from django.urls import path, include

from rest_framework import routers

from apps.accounts.views import  UserDetailsViewSet, UserRegisterViewSet


app_name = 'Accounts'

router = routers.DefaultRouter()
router.register('register', UserRegisterViewSet, basename='register')
router.register('account', UserDetailsViewSet, basename='details')

urlpatterns = [
    path('', include(router.urls)),
]