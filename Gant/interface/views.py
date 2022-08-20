import copy
import json
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from interface.logic import *
from interface.logic_models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Архив экспериментов", 'url_name': 'archive'}]


def start_page(request):
    request.session['foo'] = 'bar'
    get_start = {'start': "Начать", 'url_name': 'input_page'}
    sessia = request.session.session_key
    context = {'menu': menu,
               'title': 'start page',
               'button': get_start,
               'sessia': sessia}

    return render(request, 'interface/start_page.html', context)


def first_generatiom(request):
    pass


def data_info(request):
    if request.method == "GET":
        s = request.GET
        key = request.session.session_key
        try:
            b = Data(int(s['st1']), int(s['st2']))
            set = int(s['st3'])
            v = b.a
            stdlib = [i for i in range(len(v[0]))]
            strophic = [i for i in range(len(v))]
            sets = (int(s['st1']), int(s['st2']), int(s['st3']))
            save_to_vocabulary_sets(sets, key)

            return render(request, 'interface/data_change.html',
                          {'title': 'Редактировать данные:',
                           'date': v,  # основная табличка
                           'st': stdlib,  # станки
                           'sr': strophic,  # детали
                           'set': set,  # серии
                           'sr_num': (len(strophic) + 1),  # сколько всего деталей используется в шапке таблицы
                           'menu': menu})
        except:
            key = request.session.session_key
            print(key)
            a = read_Base(key)
            v = a[0]
            stdlib = [i for i in range(a[1][1])]
            strophic = [i for i in range(a[1][0])]
            print(a)

            return render(request, 'interface/data_change.html',
                          {'title': 'Редактировать данные:',
                           'date': v,  # основная табличка
                           'st': stdlib,  # станки
                           'sr': strophic,  # детали
                           'sr_num': (len(strophic) + 1),  # сколько всего деталей используется в шапке таблицы
                           'menu': menu})

    if request.method == "POST":
        s = request.POST
        my_list = read_get_for_experiment(s)
        key = request.session.session_key
        a = Base.objects.filter(redis=key)
        if len(a) == 0:
            print("*" * 50)
            print(a)
            add_to_Base(my_list, key)
            print("все сработал пост")
            print(s)
            print(s.__dict__)
            print(request.session.session_key)

            return redirect('experiment')
        else:
            del_from_Base_key(key)
            add_to_Base(my_list, key)
            return redirect('experiment')


def experiment(request):
    submenu = [{'title': 'редактировать сет деталей', 'url_name': 'data_info'}, ]
    key = request.session.session_key
    v = read_Base(key)
    det = v[0]
    st = v[1][0]
    st = [i for i in range(v[1][1])]
    std = [i for i in range(v[1][0])]
    print(st)
    print(std)
    context = {"details": det, 'number_st': st, 'number_det': std}

    return render(request, 'interface/turn_changer.html',
                  {'menu': menu,
                   'submenu': submenu,
                   'context': context})


def turn_result(request):
    submenu = [{'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'},
               {'title': 'таблица детали-очередность', 'url_name': 'another'},
               {'title': 'таблица рейтингов', 'url_name': 'rating'}]

    if request.method == "POST":
        key = request.session.session_key
        massiv = read_Base(key)
        data = Turn(massiv[0])
        methods = check_request(request._post)
        save_to_vocabulary_methods(methods, key)

        if type(methods) is not list:
            return HttpResponse("<h1>Выбери хотя бы один метод подачи деталей</h1>"
                                "<a href='/experiment'>Поробовать еще раз</a>")

        data.rating_use(methods, 0)
        detail_number_list = [data.r2data[i] for i in data.data]  # список из номеров деталей в порядке очереди
        details = detail_number_list
        insert_turns_to_base(key, details)

        new_list = [list(data.r2data.keys())[i] for i in details]
        mydict = dict(zip(details, new_list))

        return render(request, 'interface/turn_assert.html',
                      {'menu': menu,
                       'sr_num': len(mydict) + 2,
                       'turn3': methods,
                       'per': details,
                       'det_val': mydict,
                       'submenu': submenu})

    key = request.session.session_key
    massiv = read_Base(key)
    methods = get_methods_from_vocabulary(key)
    new_list = massiv[0]
    detail_list = read_Base2(key, new_list)
    time_detail_list = [new_list[i] for i in detail_list]

    mydict = dict(zip(detail_list, time_detail_list))

    return render(request, 'interface/turn_assert.html',
                  {'menu': menu,
                   'sr_num': len(mydict) + 2,
                   'turn3': methods,
                   'det_val': mydict,
                   'submenu': submenu})


def archive(request):
    return HttpResponse("ТУТ БУДЕТ АРХИВ")


def about(request):
    return HttpResponse("ТУТ БУДЕТ ТЗ И ПРОЧИЕ МАТЕРИАЛЫ")


def input_page(request):
    if request.method == 'GET':
        print("_______________firs_page")
        print(request)

    return render(request, 'interface/input.html', {'title': 'Ввод данных',
                                                    'menu': menu})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница модуля interface не найдена</h1>")


def turn_another_table(request):
    submenu = [{'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'},
               {'title': 'таблица очередность-детали', 'url_name': 'turn'},
               {'title': 'таблица рейтингов', 'url_name': 'rating'}]

    key = request.session.session_key
    massiv = read_Base(key)
    data = Turn(massiv[0])
    methods = get_methods_from_vocabulary(key)

    data.rating_use(methods, 0)

    new_list = [i for i in data.r2data.keys()]
    tutu = detail_turn_list(data.r2data, key)
    a = []
    for i in range(len(tutu)):
        a.append(new_list[i])

    mydict = dict(zip(tutu, a))


    return render(request, 'interface/turn_another_table.html', {'menu': menu,
                                                                 'sr_num': len(mydict) + 2,
                                                                 'turn3': methods,
                                                                 'det_val': mydict,
                                                                 'submenu': submenu})


def turn_rating_table(request):
    submenu = [{'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'},
               {'title': 'таблица очередность-детали', 'url_name': 'turn'},
               {'title': 'таблица детали-очередность', 'url_name': 'another'}, ]

    key = request.session.session_key
    massiv = read_Base(key)
    data = Turn(massiv[0])
    methods = get_methods_from_vocabulary(key)
    print(methods, "!" * 50)
    data.rating_use(methods, 0)

    stec1 = data.rdata
    stec2 = data.r2data
    stec1 = rating_table_list(methods, stec1)

    return render(request, 'interface/turn_rating_table.html', {'menu': menu,
                                                                'methods': methods,
                                                                'submenu': submenu,
                                                                'rdata': stec1,
                                                                'r2data': stec2}
                  )


def result(request):
    key = request.session.session_key
    massiv = read_Base(key)
    turn_massiv = get_from_base_turn_massiv(key)
    aturn_massiv = copy.deepcopy(turn_massiv)
    series = get_set_from_vocabulary(key)
    m = start_logic_multi((series[0], series[1]), turn_massiv, series[2])
    a={}
    for i in m:
        a["lvl_" + str(i.lvl)] = {'date': i.stec,
                                  'firstzero': i.first_nonzero,
                                  'lastnonzero': i.last_nonzero,
                                  'coefficient': calculate_effective_rating(i),
                                  }

    vocabulary = {'details':series[0],'tools':series[1],'series':series[2],'methods':get_set_from_vocabulary(key)}
    return render(request, 'interface/result.html', {'data': json.dumps(a),
                                                     'vocabulary': json.dumps(vocabulary),
                                                     'amassiv': massiv,
                                                     'turn_massiv': aturn_massiv,
                                                     'data2':a})
