from django.urls import path, include

from rest_framework import routers

from apps.accounts.views import  UserDetailsViewSet, UserRegisterViewSet


app_name = 'Accounts'

router = routers.DefaultRouter()
router.register('details', UserDetailsViewSet, basename='details')
router.register('register', UserRegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]