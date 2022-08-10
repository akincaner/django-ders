import pymysql
from django.shortcuts import render
from modules.portstatus.models import swtable
from modules.masterpage.views import json_response


def connection_mysql():
    remote_connection = pymysql.connect(host='localhost', user="testuser", password="123123", database="test_db",
                                        cursorclass=pymysql.cursors.DictCursor)
    cur = remote_connection.cursor()

    return [cur, remote_connection]


def musteriList(request):
    page = request.GET.get('page') if request.GET.get('page') else 1
    cur = connection_mysql()[0]

    if int(page) == 1:
        startLimit = 1
    else:
        startLimit = (int(page) - 1) * 10

    endLimit = int(page) * 10

    # print(startLimit)
    # print(endLimit)

    sqlquery = """
    SELECT * FROM musteri LIMIT {startLimit}, {endLimit};
    """.format(startLimit=startLimit, endLimit=endLimit)
    cur.execute(sqlquery)
    results = cur.fetchall()
    # print(results)

    countSqlQuery = """
    select count(*) as total from musteri
    """
    cur.execute(countSqlQuery)
    countResult = cur.fetchone()
    # print(countResult['total'])
    totalDataCount = int(countResult['total'])
    pageCount = round(totalDataCount / 10, 0)
    # print(pageCount)

    context = {
        "data": results,
        'pageCount': int(pageCount)
    }

    return render(request, 'musteri/musteri-liste.html', context)


def musteriEkle(request):
    cur = connection_mysql()[0]
    query = """ 
    SELECT * FROM vlan where status = 'unused'
    """
    cur.execute(query)
    # Birden Fazla Data İçin
    results = cur.fetchall()
    # Tek Bir Data için
    # cur.fetchone()

    swData = swtable.objects.all()

    context = {
        "vlanData": results,
        "swData": swData
    }

    return render(request, 'musteri/musteri-ekle.html', context)


def apiMusteriEkle(request):
    name = request.GET.get('name')
    vlan = request.GET.get('vlan')
    ip = request.GET.get('ip')
    switch = request.GET.get('switch')
    try:
        if ' ' in name:
            return json_response(status=False, message="İsim Alanında Boşluk olamaz.", data=[])

        remote_connection = pymysql.connect(host='localhost', user="testuser", password="123123", database="test_db",
                                            cursorclass=pymysql.cursors.DictCursor)
        cur = remote_connection.cursor()

        sql = """
           INSERT INTO musteri (`name`, `vlan`, `ip`,`switch`) VALUES ('{name}', '{vlan}', '{ip}','{switch}')
           """.format(name=name, vlan=vlan, ip=ip, switch=switch)

        cur.execute(sql)
        remote_connection.commit()
        return json_response(status=True, message='Data Ekleme Başarılı', data=[])
    except Exception as e:
        return json_response(status=False, message='Bir Hata Meydana Geldi.', data=[])
