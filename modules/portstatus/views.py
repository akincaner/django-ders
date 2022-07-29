from django.shortcuts import render
from modules.portstatus.models import swtable, swporttable, documents as documentsModel
from modules.portstatus.backendScript import backendScript1


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
    print(sw_data)
    context = {
        'swNameList': sw_data,
        'portlist': portlist_data,
        'portdata': port_data,
        'swSelect': int(swSelect),
        'portSelect': int(portSelect),
        'scriptResponse': scriptResponse
    }

    return render(request, 'portstatus/switch.html', context)


def documents(request):
    if request.FILES:
        for docs in request.FILES.get('dosya'):
            new_documents = documentsModel(document=docs,description=request.POST.get('subject'))
            new_documents.save()

    return render(request, 'portstatus/documents.html')
