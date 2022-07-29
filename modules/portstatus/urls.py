from django.urls import path

from modules.portstatus.views import swPortSelect, documents

# http://127.0.0.1:8000/sw/swPortSelect

urlpatterns = [
    path('swPortSelect/', swPortSelect, name="portSelect"),
    path('dokuman/', documents)
]
