from django.contrib import admin
from apps.pcData.models import pcdata, pcinfo

class pcInfos(admin.ModelAdmin):
    list_display=('name', 'description','timestamp',)
    list_display_links=('name', 'description','timestamp',)
    list_per_page = 20
    search_fields = ('name', 'description',)
    ordering=('name', 'timestamp',)

admin.site.register(pcinfo, pcInfos)

class pcDatas(admin.ModelAdmin):
    list_display=('timestamp','pc','cpu_json',)
    list_per_page = 20
    search_fields = ('pc',)
    ordering=('-timestamp',)

admin.site.register(pcdata, pcDatas)