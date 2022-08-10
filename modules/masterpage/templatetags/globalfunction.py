from django import template

register = template.Library()


@register.filter
def hideCustomerName(value,arg):
    print(value)
    name = value[:4]
    # name = name.zfill(5)
    name += arg * 3

    # print(arg)
    return name