from django.urls import path

from modules.musteri.views import musteriList, musteriEkle, apiMusteriEkle

# http://127.0.0.1:8000/musteri/switch-list/

urlpatterns = [
    path('musteri-listele/', musteriList),
    path('musteri-ekle/', musteriEkle),
    path('api/musteri-ekle/', apiMusteriEkle)
]
