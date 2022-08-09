from django.shortcuts import render
from modules.portstatus.models import swtable, swporttable, documents as documentsModel
from modules.portstatus.backendScript import backendScript1
from modules.masterpage.views import json_response


def swPortSelect(request):
    portlist_data = None
    port_data = None
    swSelect = 0
    portSelect = 0
    scriptResponse = ''

    if request.POST:

        if request.POST.get('swSelect'):
            swSelect = request.POST.get('swSelect')

            portlist_data = swporttable.objects.filter(swtabledata_id=request.POST.get('swSelect'))

        if request.POST.get('portSelect'):
            portSelect = request.POST.get('portSelect')

            port_data = swporttable.objects.get(id=request.POST.get('portSelect'))

        if swSelect != 0 and portSelect != 0:
            scriptResponse = backendScript1(port_data)

    sw_data = swtable.objects.all()
    swporttabledata = swporttable.objects.all()
    data = []
    for portData in swporttabledata:
        data.append({
            "id": portData.id,
            "port": portData.port,
            "sw_id": portData.swtabledata.id
        })
    context = {
        'swNameList': sw_data,
        'portlist': portlist_data,
        'portdata': port_data,
        'swSelect': int(swSelect),
        'portSelect': int(portSelect),
        'scriptResponse': scriptResponse,
        'swporttabledata': data
    }

    return render(request, 'portstatus/switch.html', context)


def documents(request):
    if request.FILES:
        for docs in request.FILES.get('dosya'):
            new_documents = documentsModel(document=docs, description=request.POST.get('subject'))
            new_documents.save()

    return render(request, 'portstatus/documents.html')


def getPort(request):
    data = []
    switchId = request.GET.get('switch_id')
    if switchId != '0' and switchId != None:
        portList = swporttable.objects.filter(swtabledata_id=switchId)
        for portData in portList:
            data.append({
                'id': portData.id,
                'port': portData.port
            })
        return json_response(status=True, message="", data=data)

    return json_response()
