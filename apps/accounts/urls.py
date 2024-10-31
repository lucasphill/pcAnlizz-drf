from django.urls import path, include

from rest_framework import routers

from apps.accounts.views import  UserDetailsViewSet, UserRegisterViewSet


app_name = 'Accounts'

router = routers.DefaultRouter()
# router.register('List', UserViewSet, basename='Details') #need import from apps.accounts.view
router.register('Details', UserDetailsViewSet, basename='Details')
router.register('Register', UserRegisterViewSet, basename='Register')

urlpatterns = [
    path('', include(router.urls)),
]