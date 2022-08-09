from django.urls import path

from modules.portstatus.views import swPortSelect, documents, getPort

# http://127.0.0.1:8000/sw/swPortSelect
# http://127.0.0.1:8000/sw/api/get-port

urlpatterns = [
    path('swPortSelect/', swPortSelect, name="portSelect"),
    path('dokuman/', documents),
    path('api/get-port/', getPort)
]
