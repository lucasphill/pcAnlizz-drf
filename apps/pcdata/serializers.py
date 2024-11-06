from rest_framework import serializers
from apps.pcdata.models import pcinfo, pcdata
from apps.accounts.models import User


class PcSerializer(serializers.ModelSerializer):
    choices_list=('Windows 10','Windows 11','Windows 7','Linux','MacOS','Outro')

    detail_link = serializers.SerializerMethodField()
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    other_info = serializers.CharField(required=False, default='')
    is_active = serializers.BooleanField(label='Activated')
    os = serializers.ChoiceField(choices=choices_list, label='Operational System')
    date_added = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = pcinfo
        fields = ['detail_link','id','name','other_info','os','is_active','date_added']

    def get_detail_link(self, obj): #Gera link para direcionar aos detalhes do registro pelo ID
        request = self.context.get('request')
        return request.build_absolute_uri(f'/pc/{obj.id}/')
    
    def create(self, validated_data): #Remove o campo de selecionar o usuário quando insere um registro
        validated_data['user'] = User.objects.get(id = self.context['request'].user.id)
        return super().create(validated_data)
    
class PcDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = pcdata
        fields = '__all__'
        #TODO add link para excluir registro expecifico de dados


class PcDataCpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = pcdata
        fields = ['id', 'cpu_json', 'timestamp']

class PcDataCpuLoadSerializer(serializers.ModelSerializer):
    cpu_json_load_total = serializers.SerializerMethodField()
    class Meta:
        model = pcdata
        fields = ['id', 'cpu_json_load_total', 'timestamp',]

    def get_cpu_json_load_total(self, obj): #Filtra os dados do json para apenas o cpu (que varia o nome para cada pc) e entrega apenas o load value
        json = obj.cpu_json
        cpu_name = list(json.keys())
        load = json[cpu_name[0]]['Load']['CPU Total']
        return load

    # def get_cpu_json_load_avg(self, obj): #Filtra os dados do json para apenas o cpu (que varia o nome para cada pc) e entrega apenas o load value
    #     json = obj.cpu_json
    #     cpu_name = list(json.keys())
    #     load = json[cpu_name[0]]['Load']['CPU Total']
    #     return load
    
class PcDataCpuTempSerializer(serializers.ModelSerializer):
    cpu_json_temp_pack = serializers.SerializerMethodField()
    class Meta:
        model = pcdata
        fields = ['id', 'cpu_json_temp_pack', 'timestamp',]

    def get_cpu_json_temp_pack(self, obj): #Filtra os dados do json para apenas o cpu (que varia o nome para cada pc) e entrega apenas o load value
        json = obj.cpu_json
        cpu_name = list(json.keys())
        temp = json[cpu_name[0]]['Temperature']['CPU Package']
        return temp


class PcDataGpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = pcdata
        fields = ['id', 'gpu_json', 'timestamp']

class PcDataGpuLoadSerializer(serializers.ModelSerializer):
    gpu_json_load_D3D_3D = serializers.SerializerMethodField()
    class Meta:
        model = pcdata
        fields = ['id', 'gpu_json_load_D3D_3D', 'timestamp',]

    def get_gpu_json_load_D3D_3D(self, obj): #Filtra os dados do json para apenas o cpu (que varia o nome para cada pc) e entrega apenas o load value
        json = obj.gpu_json
        gpu_name = list(json.keys())
        load = json[gpu_name[0]]['Load']['D3D 3D']
        return load

class PcDataMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = pcdata
        fields = ['id', 'memory_json', 'timestamp']
