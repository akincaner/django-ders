from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def index(request):
    context = {
        "ders": "test2",
        "tt": "test1",
        "liste": ["test1", "test2", "test3"]
    }
    return render(request, "index.html", context)


def detail(request):
    redirect_path = reverse("model")
    return redirect(redirect_path)


def getByKategoriId(request, category):
    html_text = "<h1>Hello Word</h1>"
    return HttpResponse(html_text)


def getByKategori(request, category):
    return_text = ""
    if category == 'ayakkabi':
        return_text = 'ayakkabi kategorisi'
    elif category == 'esya':
        return_text = 'Eşya Kategorisi'
    else:
        return_text = "<p> <b>" + category + "</b> Kategorisi Bulunamadı </p>"

    return HttpResponse(return_text)
