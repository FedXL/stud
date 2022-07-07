from django.http import HttpResponse, HttpResponseNotFound
from django.template import context, Template

# Create your views here.
from django.shortcuts import redirect, render
from interface.forms import *
from interface.logic import *
from interface.logic_models import *

menu = ["Панель управления","Редактировать данные","Данные","Результаты"]




def data_info(request):
    if request.method == "GET":
        if request.method == "GET":
            s = request.GET
            b = Data(int(s['st1']), int(s['st2']))
            v = b.a
            stdlib = [i for i in range(len(v[0]))]
            strophic = [i for i in range(len(v))]

            return render(request, 'interface/data_change.html',
                          {'title': 'Параметры эксперимента:',
                           'date': v,       # основная табличка
                           'st': stdlib,    # станки
                           'sr': strophic,  # детали
                           'sr_num' : (len(strophic)+1), # сколько всего деталей используется в шапке таблицы
                           'menu': menu})

def experiment(request):
    if request.method == "GET":
        s = request.GET
        full_add_to_Base(s)
        a = read_Base()
        return render(request, 'interface/experiment_choice.html',
                      {'title' : 'Параметры эксперимента:',
                       'date' : a[0],
                       'st' : [i for i in range(a[1][1])],
                       'det': [i for i in range(a[1][0])],
                       'menu' : menu,})

def result1_random(request):
    a = read_Base()
    c = a
    b = realrun(c)
    c = massiv_to_stec_massiv(b)

    return render(request, 'interface/result_1_random.html',
                      {'title' : 'Random',
                       'date' : a[0],
                       'st' : [i for i in range(a[1][1])],
                       'det': [i for i in range(a[1][0])],
                       'menu' : menu,
                       'gant': c})

def test(request):
    if request.method =='POST':
        print(request)
        return redirect('')




def first_page(request):
    if request.method =='GET':
        print("_______________firs_page")
        print(request)
    return render(request, 'interface/about.html', {'title': 'О сайте',
                                                    'menu': menu})

"""
def interface(request):
    return HttpResponse("<h1> Гениально сир </h1>")

def categories(request,catid):
    return HttpResponse(f" <h1> CATS </h1> <br> кошка номер : {catid}")

def archive(request,year):
    if int(year)>3000:
        return redirect('home', permanent=False)

    return HttpResponse(f"<h1> ГОД {year}</h1>")
"""

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница модуля interface не найдена</h1>")
