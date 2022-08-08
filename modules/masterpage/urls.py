from django.urls import path

from modules.masterpage.views import buildMasterpage, login, loginPage,logout

# http://127.0.0.1:8000/logout/


urlpatterns = [
    path('', buildMasterpage,name="masterpage"),
    path('api/login/', login),
    path('login/', loginPage,name="loginpage"),
    path('logout/', logout)
]