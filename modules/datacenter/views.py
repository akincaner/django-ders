from django.shortcuts import render
from modules.datacenter.models import dc


def showDc(request):

    print(request.POST.get('dc'))

    dc_data = dc.objects.all()
    context = {
        'dcData': dc_data
    }
    return render(request, 'index.html', context)
