from rest_framework import serializers
from apps.pcData.models import pcdata, pcinfo

class PcInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = pcinfo
        fields = ['id','user','name','description','timestamp']

# class PcDataSerializer(serializers.HyperlinkedModelSerializer):
class PcDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = pcdata
        fields = ['id','pc','cpu_json','gpu_json','memory_json','timestamp']