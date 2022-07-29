from django.http import HttpResponse
from django.shortcuts import render
from modules.datacenter.models import dc
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from modules.masterpage.views import json_response



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
    return render(request, 'datacener/index.html', context)


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
    return render(request, 'datacener/dc2.html', context)


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

