from django.urls import path

from modules.masterpage.views import buildMasterpage, login, loginPage, logout, ipSorgula, buildNewTemp

# http://127.0.0.1:8000/logout/
# http://127.0.0.1:8000/


urlpatterns = [
    path('', buildMasterpage, name="masterpage"),
    path('api/login/', login),
    path('login/', loginPage, name="loginpage"),
    path('logout/', logout),
    path('ip-sorgula/', ipSorgula),
    path('yeni-template/', buildNewTemp)
]
