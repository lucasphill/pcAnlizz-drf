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
ROUTES AVAILABLE
Developed routes until now

User routes:
register/

account/
account/uuid:pk/
account/resetpassword/ (In progress)

PC routes:
pc/
pc/active/
pc/uuid:pk/

Data routes:
pc/uuid:pk/data/

CPU Data
pc/uuid:pk/data/cpu/

pc/uuid:pk/data/cpu/load/
pc/uuid:pk/data/cpu/load/avr/
pc/uuid:pk/data/cpu/load/avr/?time=30

pc/uuid:pk/data/cpu/temp/
pc/uuid:pk/data/cpu/temp/avr/
pc/uuid:pk/data/cpu/temp/avr/?time=30

pc/uuid:pk/data/cpu/temp/max/
pc/uuid:pk/data/cpu/temp/max/?time=30

MEMORY Data
pc/uuid:pk/data/memory/
pc/uuid:pk/data/memory/avr/
pc/uuid:pk/data/memory/avr/?time=30

GPU Data
pc/uuid:pk/data/gpu/

pc/uuid:pk/data/gpu/temp/
pc/uuid:pk/data/gpu/temp/avr/
pc/uuid:pk/data/gpu/temp/avr/?time=30

pc/uuid:pk/data/gpu/load/
pc/uuid:pk/data/gpu/load/avr/
pc/uuid:pk/data/gpu/load/avr/?time=30

pc/uuid:pk/data/gpu/memory/
pc/uuid:pk/data/gpu/memory/avr/
pc/uuid:pk/data/gpu/memory/avr/?time=30
'''