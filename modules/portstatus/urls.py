from django.urls import path

from modules.portstatus.views import swPortSelect

# http://127.0.0.1:8000/dc

urlpatterns = [
    path('swPortSelect/', swPortSelect)
]