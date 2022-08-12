import math
import pymysql
from django.shortcuts import render
from modules.portstatus.models import swtable
from modules.masterpage.views import json_response

import logging

errorLog = logging.getLogger('custom-error')


def connection_mysql():
    remote_connection = pymysql.connect(host='localhost', user="testuser", password="123123", database="test_db",
                                        cursorclass=pymysql.cursors.DictCursor)
    cur = remote_connection.cursor()

    return [cur, remote_connection]


def musteriList(request):
    page = request.GET.get('page') if request.GET.get('page') else 1

    # print(request.GET.get('size'))
    if request.GET.get('size'):
        size = int(request.GET.get('size'))
    else:
        size = 10

    # print(size)

    cur = connection_mysql()[0]

    if int(page) == 1:
        startLimit = 1
    else:
        startLimit = (int(page) - 1) * size

    endLimit = int(page) * size

    # print(startLimit)
    # print(endLimit)

    sqlquery = """
    SELECT * FROM musteri LIMIT {size} OFFSET {startLimit};
    """.format(size=size, startLimit=startLimit)

    # print(sqlquery)
    # infoLog = logging.getLogger('custom-info')
    errorLog.error(sqlquery)

    cur.execute(sqlquery)
    results = cur.fetchall()
    # print(results)
    # print(len(results))

    countSqlQuery = """
    select count(*) as total from musteri
    """
    cur.execute(countSqlQuery)
    countResult = cur.fetchone()
    # print(countResult['total'])
    totalDataCount = int(countResult['total'])
    # pageCount = round(totalDataCount / 10, 0)
    pageCount = math.ceil(totalDataCount / size)

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
    update = request.GET.get('update')
    id = request.GET.get('id')
    try:
        if ' ' in name:
            return json_response(status=False, message="İsim Alanında Boşluk olamaz.", data=[])

        remote_connection = pymysql.connect(host='localhost', user="testuser", password="123123", database="test_db",
                                            cursorclass=pymysql.cursors.DictCursor)
        cur = remote_connection.cursor()

        if update:
            sql = """
                UPDATE musteri SET name = '{name}' , vlan= '{vlan}', ip='{ip}', switch='{switch}' WHERE (id = {id});
            """.format(name=name, vlan=vlan, ip=ip, switch=switch, id=id)
        else:
            sql = """
               INSERT INTO musteri (`name`, `vlan`, `ip`,`switch`) VALUES ('{name}', '{vlan}', '{ip}','{switch}')
               """.format(name=name, vlan=vlan, ip=ip, switch=switch)

        cur.execute(sql)
        remote_connection.commit()
        return json_response(status=True, message='Data Ekleme Başarılı', data=[])
    except Exception as e:
        # print(e)
        errorLog.error(e)
        return json_response(status=False, message='Bir Hata Meydana Geldi.', data=[])


def musteriRevize(request):
    cur = connection_mysql()[0]

    sqlquery = """
        SELECT * FROM musteri;
        """
    cur.execute(sqlquery)
    results = cur.fetchall()

    print(results)

    query = """ 
      SELECT * FROM vlan where status = 'unused'
      """
    cur.execute(query)
    vlanData = cur.fetchall()

    swData = swtable.objects.all()

    context = {
        "musteriData": results,
        "vlanData": vlanData,
        "swData": swData
    }

    return render(request, 'musteri/musteri-revize.html', context)


def musterFilter(request):
    ipKeyword = request.GET.get('ipKeyword')
    swKeyword = request.GET.get('swKeyword')

    cur = connection_mysql()[0]
    sqlquery = """ 
        SELECT * FROM musteri where 
            (
            ip like '%{ip}%'
            and 
            switch like '%{sw}%'
            );
        """.format(ip=ipKeyword, sw=swKeyword)
    cur.execute(sqlquery)
    results = cur.fetchall()

    return json_response(status=True, message='', data=results)


def musteriDataTable(request):
    cur = connection_mysql()[0]
    sqlquery = """
        SELECT * FROM musteri 
        """
    cur.execute(sqlquery)
    results = cur.fetchall()
    context = {
        "data": results,
    }
    return render(request, 'musteri/musteri-data-table.html', context)
