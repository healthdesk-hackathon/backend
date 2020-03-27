from django.urls import include, path
from api.urls_v1 import urlpatterns as urls_v1

urlpatterns = [
    path('v1/', include((urls_v1, 'v1'), namespace='v1')),
]
