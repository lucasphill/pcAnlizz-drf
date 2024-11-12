from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view

from django.db import connection

import json

from apps.pcdata.models import pcinfo, pcdata
from apps.pcdata.serializers import PcSerializer, PcDataSerializer, PcDataCpuSerializer, PcDataGpuSerializer, PcDataMemorySerializer, PcDataCpuLoadSerializer, \
    PcDataCpuTempSerializer, PcDataGpuLoadSerializer, PcDataGpuTempSerializer, PcDataGpuMemorySerializer
from rest_framework.response import Response

#TODO Adicionar comentários nas funções e actions e limpar o codigo
def get_cpu_name(pk):
    get_key = f"SELECT jsonb_object_keys(cpu_json) FROM pcdata_pcdata WHERE pc_id='{pk}' LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(get_key)
        results2 = cursor.fetchall()
        cpu_name = results2[0][0]
        return cpu_name
    
def get_gpu_name(pk):
    get_key = f"SELECT jsonb_object_keys(gpu_json) FROM pcdata_pcdata WHERE pc_id='{pk}' LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(get_key)
        results2 = cursor.fetchall()
        gpu_name = results2[0][0]
        return gpu_name
    
def get_memory_name(pk):
    get_key = f"SELECT jsonb_object_keys(memory_json) FROM pcdata_pcdata WHERE pc_id='{pk}' LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(get_key)
        results2 = cursor.fetchall()
        memory_name = results2[0][0]
        return memory_name

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
    

    @action(methods=['get'], detail=True, url_path='data/cpu/load', url_name='data-cpu-load')
    def cpu_load(self, request, pk):
        
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataCpuLoadSerializer(queryset, many=True,)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True, url_path='data/cpu/load/avg', url_name='data-cpu-load-avg')
    def cpu_load_avg(self, request, pk):
        time = self.request.query_params.get('time')

        cpu_name = get_cpu_name(pk)

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

    @action(methods=['get'], detail=True, url_path='data/cpu/temp/avg', url_name='data-cpu-temp-avg')
    def cpu_temp_avg(self, request, pk):
        time = self.request.query_params.get('time')

        cpu_name = get_cpu_name(pk)

        if time:
            query = f"SELECT AVG((jsonb_extract_path_text(cpu_json, '{cpu_name}', 'Temperature', 'Core Average'))::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT AVG((jsonb_extract_path_text(cpu_json, '{cpu_name}', 'Temperature', 'Core Average'))::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'cpu_temp_avg': results[0][0]})
    
    @action(methods=['get'], detail=True, url_path='data/cpu/temp/max', url_name='data-cpu-temp-max')
    def cpu_temp_max(self, request, pk):
        time = self.request.query_params.get('time')

        cpu_name = get_cpu_name(pk)

        if time:
            query = f"SELECT MAX((jsonb_extract_path_text(cpu_json, '{cpu_name}', 'Temperature', 'Core Max'))::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT MAX((jsonb_extract_path_text(cpu_json, '{cpu_name}', 'Temperature', 'Core Max'))::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'cpu_temp_max': results[0][0]})



    @action(methods=['get'], detail=True, url_path='data/memory', url_name='data-memory',)
    def memory(self, request, pk):
        # queryset = pcdata.objects.raw(f"SELECT id, memory_json, timestamp FROM pcdata_pcdata WHERE pc_id='{pk}' ORDER BY timestamp DESC")
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataMemorySerializer(queryset, many=True,)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True, url_path='data/memory/avg', url_name='data-memory-avg',)
    def memory_avg(self, request, pk):
        time = self.request.query_params.get('time')

        memory_name = get_memory_name(pk)

        if time:
            query = f"SELECT AVG((memory_json->'{memory_name}'->'Load'->'Memory')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT AVG((memory_json->'{memory_name}'->'Load'->'Memory')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'memory_avg': results[0][0]})



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
    
    @action(methods=['get'], detail=True, url_path='data/gpu/load/avg', url_name='data-gpu-load-avg')
    def gpu_load_avg(self, request, pk):
        time = self.request.query_params.get('time')

        gpu_name = get_gpu_name(pk)

        if time:
            query = f"SELECT AVG((gpu_json->'{gpu_name}'->'Load'->'D3D 3D')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT AVG((gpu_json->'{gpu_name}'->'Load'->'D3D 3D')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'gpu_load_avg': results[0][0]})
    

    @action(methods=['get'], detail=True, url_path='data/gpu/temp', url_name='data-gpu-temp')
    def gpu_temp(self, request, pk):
        # queryset = pcdata.objects.raw(f"SELECT id, cpu_json->'Intel Core i7-9700KF'->'Load'->'CPU Total' as cpu_total, timestamp FROM pcdata_pcdata WHERE pc_id='{pk}' ORDER BY timestamp DESC")
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataGpuTempSerializer(queryset, many=True,)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True, url_path='data/gpu/temp/avg', url_name='data-gpu-temp-avg')
    def gpu_temp_avg(self, request, pk):
        time = self.request.query_params.get('time')

        gpu_name = get_gpu_name(pk)

        if time:
            query = f"SELECT AVG((gpu_json->'{gpu_name}'->'Temperature'->'GPU Core')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT AVG((gpu_json->'{gpu_name}'->'Temperature'->'GPU Core')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'gpu_temp_avg': results[0][0]})


    @action(methods=['get'], detail=True, url_path='data/gpu/memory', url_name='data-gpu-memory')
    def gpu_memory(self, request, pk):
        queryset = pcdata.objects.filter(pc=pk).order_by('-timestamp')
        serializer = PcDataGpuMemorySerializer(queryset, many=True,)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True, url_path='data/gpu/memory/avg', url_name='data-gpu-memory-avg')
    def gpu_memory_avg(self, request, pk):
        time = self.request.query_params.get('time')

        gpu_name = get_gpu_name(pk)

        if time:
            query = f"SELECT AVG((gpu_json->'{gpu_name}'->'Load'->'GPU Memory')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}' and timestamp > current_date - interval '{time}' day;"
        else:
            query = f"SELECT AVG((gpu_json->'{gpu_name}'->'Load'->'GPU Memory')::numeric) FROM pcdata_pcdata WHERE pc_id='{pk}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return Response({'gpu_temp_avg': results[0][0]})




@api_view(['POST'])
def post_data(request):
    """Função responsavel por receber via post os valores enviados do Client no computador do usuário e inserir no banco de dados"""
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