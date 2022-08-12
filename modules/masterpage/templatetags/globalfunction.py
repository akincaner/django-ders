from django import template

register = template.Library()


@register.filter
def hideCustomerName(value,arg):
    # print(value)
    name = value[:4]
    # name = name.zfill(5)
    name += arg * 3

    # print(arg)
    return name

@register.filter
def getpath(request):
    if request.GET:
        print(request.GET.get('page'))
    return ''



@register.filter
def getSizeFromParams(request):
    if request.GET:
        if request.GET.get('size'):
            return request.GET.get('size')
    return '10'
