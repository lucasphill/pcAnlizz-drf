from django.urls import path, include

from rest_framework import routers

from apps.pcData.views import *

app_name = 'pcAnlizz'

router = routers.DefaultRouter()
router.register('pcinfo', PcInfoViewSet)
router.register('pcdata', PcDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]