from django.urls import path

from modules.datacenter.views import showDc, addDc, addNewDc, dcApi, login

# http://127.0.0.1:8000/dc

urlpatterns = [
    path('dc/', showDc),
    path('dc2/', addDc),
    path('add-new-dc/', addNewDc),
    path('api/dc/', dcApi),
    path('api/login/', login)
]
