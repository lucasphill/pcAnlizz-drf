from rest_framework import viewsets

from apps.pcData.models import *
from apps.pcData.serializers import *

class PcInfoViewSet(viewsets.ModelViewSet):
    queryset = pcinfo.objects.all()
    serializer_class = PcInfoSerializer

class PcDataViewSet(viewsets.ModelViewSet):
    queryset = pcdata.objects.all()
    serializer_class = PcDataSerializer