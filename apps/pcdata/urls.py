from django.urls import path, include

from rest_framework import routers

from apps.pcdata.views import PcViewSet, post_data


app_name = 'Pc Data'

router = routers.DefaultRouter()
router.register('pc', PcViewSet, basename='pc')

urlpatterns = [
    path('', include(router.urls)),
    path('pc/active/', PcViewSet.as_view({'get': 'active'}), name='pc-active'),
    path('post-data/', post_data, name='post-data'),
]

'''   
User: 
# path('register/', - tela de registro do usuário

# path('account/', - dados do usuario
# path('account/<uuid:pk>/', - put do usuario
path('account/resetpassword/', - tela de registro do usuário

Data:
# path('pc/', - todos pcs do usuario - ok
# path('pc/active', - todos pcs ativos do usuario - ok

# path('pc/<uuid:pk>/', - todos dados do pc especificado do usuário - ok

# path('pc/<uuid:pk>/data', - dados json (cpu, gpu, memory) do pc especificado do usuário

# path('pc/<uuid:pk>/data/cpu/', - dados json de cpu de todos os tempos - ok
# path('pc/<uuid:pk>/data/cpu/load/', - dados json de cpu referente ao uso (load) de todos os tempos - ok
# path('pc/<uuid:pk>/data/cpu/load/avr/', - media dos dados json de cpu referente ao uso (load) de todos os tempos - ok
# path('pc/<uuid:pk>/data/cpu/load/avr/?time=30', - media dos dados json de cpu referente ao uso (load) no tempo especificado - ok

# path('pc/<uuid:pk>/data/cpu/temp', - dados json de cpu referente a temperatura de todos os tempos - ok
# path('pc/<uuid:pk>/data/cpu/temp/avr', - media dos dados json de cpu referente a temperatura de todos os tempos - ok
# path('pc/<uuid:pk>/data/cpu/temp/avr/<int:days>', - media dos dados json de cpu referente a temperatura no tempo especificado - ok
# path('pc/<uuid:pk>/data/cpu/temp/avr/<int:days>/?time=30', - media dos dados json de cpu referente a temperatura no tempo especificado - ok
# path('pc/<uuid:pk>/data/cpu/temp/max/<int:days>', - maxima dos dados json de cpu referente a temperatura no tempo especificado - ok
# path('pc/<uuid:pk>/data/cpu/temp/max/<int:days>/?time=30', - maxima dos dados json de cpu referente a temperatura no tempo especificado - ok

# path('pc/<uuid:pk>/data/memory/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/memory/avr/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/memory/avr/<int:days>', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok

# path('pc/<uuid:pk>/data/gpu/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/temp/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/temp/avr/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/temp/avr/<int:days>', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/load/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado)
# path('pc/<uuid:pk>/data/gpu/load/avr/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/load/avr/<int:days>', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/memory/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/memory/avr/', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
# path('pc/<uuid:pk>/data/gpu/memory/avr/<int:days>', - get registros de temp maxima dos ultimos 30 dias (ou tempo especificado) - ok
'''