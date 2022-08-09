import json

from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def json_response(status=False, message="", data={}):
    JsonData = {"status": status, "message": message, "data": data}
    JsonData = json.dumps(JsonData, cls=DjangoJSONEncoder)
    return HttpResponse(JsonData)


def buildMasterpage(request):
    if request.user.is_anonymous:
        redirect_path = reverse("loginpage")
        return redirect(redirect_path)
    return render(request, 'dashboard.html')


@csrf_exempt
def login(request):
    data = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    returnHtml = request.POST.get('returnHtml')
    # print(username)
    # print(password)
    # print(returnHtml)
    try:
        remoteUser = User.objects.get(username=username)
        authenticatedUser = authenticate(username=username, password=password)
        if authenticatedUser is None:
            return json_response(status=False, message="Şifreniz Hatalı")
        if authenticatedUser.is_active:
            authenticatedUser.backend = "django.contrib.auth.backends.ModelBackend"
            do_login(request, authenticatedUser)
            groups = authenticatedUser.groups.all()
            userGroups = []
            for grp in groups:
                userGroups.append(grp.name)

            data = {
                'id': str(authenticatedUser.id),
                'token': str(request.session.session_key),
                'groups': userGroups
            }
            if returnHtml == 'true':
                redirect_path = reverse("masterpage")
                return redirect(redirect_path)
            return json_response(status=True, data=data)
        else:
            return json_response(status=False, message="Kullanıcı Etkin Değil")
    except ObjectDoesNotExist:
        return json_response(status=False, message="Kullanıcı Adı Hatalı")
    except Exception as e:
        print(e)

    return json_response()


def loginPage(request):
    print(request.user)
    if not request.user.is_anonymous:
        # print(request.user.groups.all())
        # print(request.user.first_name)
        # print(request.user.last_name)
        # print(request.user.email)
        redirect_path = reverse("masterpage")
        return redirect(redirect_path)
    return render(request, 'login.html')


def logout(request):
    do_logout(request)
    redirect_path = reverse("loginpage")
    return redirect(redirect_path)


def ipSorgula(request):
    data = {
        "code": 200,
        "success": True,
        "data": [
            "198.18.2.0/21",
            "198.18.2.16/22",
            "198.18.2.32/23",
            "198.18.2.48/24",
            "198.18.2.64/25",
            "198.18.2.80/26",
            "198.18.2.96/27",
            "198.18.2.112/28",
            "198.18.2.128/21",
            "198.18.2.144/22",
            "198.18.2.160/23",
            "198.18.2.176/24",
            "198.18.2.192/25",
            "198.18.2.208/26",
            "198.18.2.224/27",
            "198.18.2.240/28"
        ],
        "time": 0.003
    }
    JsonData = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(JsonData)
