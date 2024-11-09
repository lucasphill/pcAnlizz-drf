from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view

from django.db import connection

import json

from apps.pcdata.models import pcinfo, pcdata
from apps.pcdata.serializers import PcSerializer, PcDataSerializer, PcDataCpuSerializer, PcDataGpuSerializer, PcDataMemorySerializer, PcDataCpuLoadSerializer, \
    PcDataCpuTempSerializer, PcDataGpuLoadSerializer
from rest_framework.response import Response


'''
todos os computadores usuario logado
todos computadores ativos usuário logado
'''

class PcViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post', 'put', 'delete']
    
    serializer_class = PcSerializer

    def get_queryset(self): #Gera uma queryset somente com os computadores do usuário logado
        user_id = self.request.user.id
        return pcinfo.objects.filter(user=user_id).order_by('-name')
    
    #TODO Criar rota no home para essa function se possivel
    @action(methods=['get'], detail=False, url_path='active', url_name='active',)
    def active(self, request): #Gera uma queryset com apenas os computadores ativos do usuário logado
        user_id = self.request.user.id #Pega o id da sessão
        queryset = pcinfo.objects.filter(user=user_id, is_active=True) #Gera a query
        serializer = PcSerializer(queryset, many=True, context={'request': request}) #Serializa a pesquisa/query, context permite o link do serializador (verificar)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True, url_path='data', url_name='data',)
    def data(self, request, pk):
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataSerializer(queryset, many=True,)
        return Response(serializer.data)
    


    @action(methods=['get'], detail=True, url_path='data/cpu', url_name='data-cpu',)
    def cpu(self, request, pk):
        # queryset = pcdata.objects.raw(f"SELECT id, cpu_json, timestamp FROM pcdata_pcdata WHERE pc_id='{pk}' ORDER BY timestamp DESC")
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataCpuSerializer(queryset, many=True,)
        return Response(serializer.data)
    
    #SELECT id, cpu_json->'Intel Core i7-9700KF'->'Load'->'CPU Total' as cpu_total, timestamp FROM pcdata_pcdata WHERE pc_id='5035c8dc-cd09-45c2-ba3e-050b64647cbf' ORDER BY timestamp DESC
    @action(methods=['get'], detail=True, url_path='data/cpu/load', url_name='data-cpu-load')
    def cpu_load(self, request, pk):
        
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataCpuLoadSerializer(queryset, many=True,)
        return Response(serializer.data)
    
    #TODO CORRIGIR QUERY COM ID DO PC CORRETO
    #SELECT AVG((cpu_json->'Intel Core i7-9700KF'->'Load'->'CPU Total')::numeric) FROM pcdata_pcdata WHERE pc_id='5035c8dc-cd09-45c2-ba3e-050b64647cbf'
    @action(methods=['get'], detail=True, url_path='data/cpu/load/avg', url_name='data-cpu-load-avg')
    def cpu_load_avg(self, request, pk):
        time = self.request.query_params.get('time')
        print(time)
        #TODO Melhorar essa função para pegar a keyvalue de diferentes processadores na chave
        get_key = f"SELECT jsonb_object_keys(cpu_json) FROM pcdata_pcdata WHERE pc_id='{pk}' LIMIT 1"
        with connection.cursor() as cursor:
            cursor.execute(get_key)
            results2 = cursor.fetchall()
            cpu_name = results2[0][0]

        if time:
            query = f"SELECT AVG((cpu_json->'{cpu_name}'->'Load'->'CPU Total')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT AVG((cpu_json->'{cpu_name}'->'Load'->'CPU Total')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'cpu_load_avg': results[0][0]})

    @action(methods=['get'], detail=True, url_path='data/cpu/temp', url_name='data-cpu-temp')
    def cpu_temp(self, request, pk):
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataCpuTempSerializer(queryset, many=True,)
        return Response(serializer.data)



    @action(methods=['get'], detail=True, url_path='data/gpu', url_name='data-gpu',)
    def gpu(self, request, pk):
        # queryset = pcdata.objects.raw(f"SELECT id, gpu_json, timestamp FROM pcdata_pcdata WHERE pc_id='{pk}' ORDER BY timestamp DESC")
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataGpuSerializer(queryset, many=True,)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True, url_path='data/gpu/load', url_name='data-gpu-load')
    def gpu_load(self, request, pk):
        # queryset = pcdata.objects.raw(f"SELECT id, cpu_json->'Intel Core i7-9700KF'->'Load'->'CPU Total' as cpu_total, timestamp FROM pcdata_pcdata WHERE pc_id='{pk}' ORDER BY timestamp DESC")
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataGpuLoadSerializer(queryset, many=True,)
        return Response(serializer.data)
   


    @action(methods=['get'], detail=True, url_path='data/memory', url_name='data-memory',)
    def memory(self, request, pk):
        

        # queryset = pcdata.objects.raw(f"SELECT id, memory_json, timestamp FROM pcdata_pcdata WHERE pc_id='{pk}' ORDER BY timestamp DESC")
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataMemorySerializer(queryset, many=True,)
        return Response(serializer.data)



@api_view(['POST'])
def post_data(request):
    """Função responsavel por receber via post os valores enviados do Client no computador do usuário"""
    if request.method == 'POST':
        
        request_data = request.body #bytes - recebe do json enviado pelo post
        data = request_data.decode('utf8') #str
        dict_data = json.loads(data) #dict

        cpu_data = json.dumps(dict_data['cpu_json']) #str e separa o valor de cpu_json
        gpu_data = json.dumps(dict_data['gpu_json']) #str e separa o valor de gpu_json
        memory_data = json.dumps(dict_data['memory_json']) #str e separa o valor de memory_json
        uuid = dict_data['pc_uuid'] #str e separa o valor de pc_uuid

        query = f"""INSERT INTO pcdata_pcdata (id, cpu_json, gpu_json, memory_json, "timestamp", pc_id) VALUES (gen_random_uuid(), '{cpu_data}', '{gpu_data}', '{memory_data}', now(), '{uuid}');"""

        with connection.cursor() as cursor:
            cursor.execute(query)

        return Response({request_data}, status=status.HTTP_201_CREATED)