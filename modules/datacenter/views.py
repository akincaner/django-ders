import json
from django.http import HttpResponse
from django.shortcuts import render
from modules.datacenter.models import dc
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as do_login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session


def json_response(status=False, message="", data={}):
    JsonData = {"status": status, "message": message, "data": data}
    JsonData = json.dumps(JsonData, cls=DjangoJSONEncoder)
    return HttpResponse(JsonData)


def stringManuplation(string):
    string.replace('ü', 'u')
    string.replace('ı', 'i')
    string.replace('ö', 'o')
    return string


def showDc(request):
    postData = None
    if request.POST:
        postData = dc.objects.get(id=request.POST.get('selectedDc'))

    dc_data = dc.objects.all()
    context = {
        'dcData': dc_data,
        'filterData': postData
    }
    return render(request, 'index.html', context)


def addDc(request):
    filterData = None
    showForm = False
    if request.POST:
        if request.POST.get('selectedDc') == 'yeniEkle':
            showForm = True
        else:
            filterData = dc.objects.get(id=request.POST.get('selectedDc'))

    dc_data = dc.objects.all()
    context = {
        'dcData': dc_data,
        'filterData': filterData,
        'showForm': showForm
    }
    return render(request, 'dc2.html', context)


def addNewDc(request):
    if request.POST:
        try:
            newdc = dc(
                location=request.POST.get('dclocation'),
                name=stringManuplation(request.POST.get('dcname')),
                tip=request.POST.get('type'),
                domain=request.POST.get('domain')
            )
            newdc.save()
            return HttpResponse('Veri Ekleme Başarılı')
        except Exception as e:
            print(e)
            return HttpResponse('Veri Ekleme Hatalı')
    else:
        return HttpResponse('Veri Bulunamadı')


#
# {
#    "status":True,
#    "message": '',
#    "data": {} veya []
# }
#

# select * from dc where dc.domain = 'fixed' and location like 'İstanbul'


def get_user(token):
    try:
        session = Session.objects.get(session_key=token)
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        print(e)
        return False



def dcApi(request):
    status = False
    message = ''
    data = []
    user = get_user(request.GET.get('token'))
    if user == False:
        return json_response(status=False, message='Kullanıcı Bulunamadı')
    else:
        if len(user.groups.filter(name='Api')) > 0:
            try:
                if request.GET.get('domain') and request.GET.get('lokasyon'):
                    dcData = dc.objects.filter(domain=request.GET.get('domain'),
                                               location__icontains=request.GET.get('lokasyon'))
                else:
                    dcData = dc.objects.all()
                for item in dcData:
                    data.append({
                        "dc_adi": item.name,
                        "dc_lokasyon": item.location,
                        "dc_domain": item.domain
                    })
                status = True
                message = 'İşlem Başarılı'
            except Exception as e:
                print(e)
                message = e
        else:
            return json_response(status=False, message='Kullanıcı İzini Yetersiz')


    return json_response(status=status, message=message, data=data)


@csrf_exempt
def login(request):
    data = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
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
            return json_response(status=True, data=data)
        else:
            return json_response(status=False, message="Kullanıcı Etkin Değil")
    except ObjectDoesNotExist:
        return json_response(status=False, message="Kullanıcı Adı Hatalı")
    except Exception as e:
        print(e)

    return json_response()
