
from django.urls import path

from modules.datacenter.views import showDc

# http://127.0.0.1:8000/dc

urlpatterns = [
    path('dc/', showDc)
]
