from django.contrib import admin

from apps.pcdata.models import pcinfo, pcdata

class PcInfos(admin.ModelAdmin):
    list_display = ('name','other_info','os','is_active','date_added',)
    list_display_links = ('name','other_info','os',)
    list_per_page = 20
    search_fields = ('name','other_info','os',)
    ordering = ('name',)

admin.site.register(pcinfo, PcInfos)