import copy
import json
from django.http.request import HttpRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import CreateView
from interface.logic import *
from interface.logic_models import *
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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
    """
    три режима работы обработчика

    1- прихододит GET и генерит первый раз сет деталей
    2- приходит пустой GET (это перенаправление с более поздних этапов) read from bd
    3- приходит POST (отредактированная пользователем таблица ) save to bd and redirect to experiment

    """

    if request.method == "GET":
        # Вариант-1 при заполненном GET генерим СЕТ из деталей.
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
                           'menu': menu,
                           'submenu': 'input_page'})
        except:
            # Вариант-2 при пустом GET вытаскивам сет из бд

            key = request.session.session_key
            if request.headers.get('Referer').split("/")[3] == 'archive':
                user = request.user
                record_id = request.GET.get('record_id')
                record_id = int(record_id)
                arch_base = get_from_archive(request)
                for i in arch_base:
                    per = i.get('id')
                    if per == record_id:
                        new_dataset = i.get('data')
                        num_of_details = i.get('details')
                        num_of_tools = i.get('tools')
                        series = i.get('series')
                        break
                v = new_dataset

                stdlib = [i for i in range(len(new_dataset[0]))] # станки
                strophic = [i for i in range(len(new_dataset))]  # детали
                sets = (len(new_dataset))
                save_to_vocabulary_sets([num_of_details, num_of_tools, series], key)

            else:
                a = read_Base(key)
                v = a[0]
                stdlib = [i for i in range(a[1][1])] # станки
                strophic = [i for i in range(a[1][0])] # детали

            return render(request, 'interface/data_change.html',
                          {'title': 'Редактировать данные:',
                           'date': v,  # основная табличка
                           'st': stdlib,  # станки
                           'sr': strophic,  # детали
                           'sr_num': (len(strophic) + 1),  # сколько всего деталей используется в шапке таблицы
                           'menu': menu})

    if request.method == "POST":
        # Вариант-3 сохраняем СЕТ в бд
        #if request.headers.get('Referer').split("/")[3]) == 'archive':

        s = request.POST
        my_list = read_get_for_experiment(s)
        key = request.session.session_key
        a = Base.objects.filter(redis=key)
        if len(a) == 0:
            add_to_Base(my_list, key)
            return redirect('experiment')
        else:
            del_from_Base_key(key)
            add_to_Base(my_list, key)
            return redirect('experiment')


def experiment(request):
    submenu = [{'title': 'ввод данных ', 'url_name': 'input_page'},
               {'title': 'редактировать сет деталей', 'url_name': 'data_info'}, ]

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
    """ Всего 2 режима работы
    1. по направлению на страницу, все данные вытаскиваются из бд
    2. после редактирования данных пользователя, все правки сохраняются в бд
    и перенаправление turn_assert
    """

    submenu = [{'title': 'ввод данных ', 'url_name': 'input_page'},
               {'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'},
               ]
    subsubmenu = [{'title': 'таблица детали-очередность', 'url_name': 'another'},
                  {'title': 'таблица рейтингов', 'url_name': 'rating'}]
    # 2й вариант
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
                       'sr_num': len(list(mydict.values())[0]) + 2,
                       'turn3': methods,
                       'per': details,
                       'det_val': mydict,
                       'tools_series': list(mydict.values())[0],
                       'submenu': submenu,
                       'submenu2': subsubmenu})
    #1й вариант
    key = request.session.session_key
    massiv = read_Base(key)
    methods = get_methods_from_vocabulary(key)
    new_list = massiv[0]
    detail_list = read_Base2(key, new_list)
    print('!' * 150)
    print("detail_list", detail_list)
    print("new_list", new_list)
    time_detail_list = [new_list[i] for i in detail_list]
    mydict = dict(zip(detail_list, time_detail_list))

    return render(request, 'interface/turn_assert.html',
                  {'menu': menu,
                   'sr_num': len(list(mydict.values())[0]) + 2,
                   'turn3': methods,
                   'det_val': mydict,
                   'tools_series': list(mydict.values())[0],
                   'submenu': submenu,
                   'submenu2': subsubmenu})


def archive(request: HttpRequest):
    text, context = {}, {}
    if request.user.is_authenticated:
        if request.method == "POST" and request.POST.get('logic') == "get":

            return redirect('data_info')

        elif request.method == "POST":
            add_to_archive(request)
            return HttpResponse("<h1>Данные успешно сохранены</h1>"
                                "<a href='/result'>Вернуться</a>")
        if request.method == "GET" and request.GET.get('record_id') is not None:
            print("YYEEEES THAT WOOOOOOOOOOORKS!!!!!!!!!!!!")
            print(request.GET.get('record_id'))
            del_records_from_archive(request)
            return redirect('archive')
        else:
            context = get_from_archive(request)
            text['h1'] = "Архив"
    else:
        text['h1'] = "Пожалуйста авторизируйтесь"
    return render(request, 'interface/archive.html', {'menu': menu,
                                                      'context': context,
                                                      'texts': text
                                                      })


def about(request):
    return render(request, 'interface/1s.html', {'title': 'О сайте'})


def input_page(request):
    if request.method == 'GET':
        print("_______________firs_page")
        print(request)

    return render(request, 'interface/input.html', {'title': 'Ввод данных',
                                                    'menu': menu})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница модуля interface не найдена</h1>")


def turn_another_table(request):
    submenu = [{'title': 'ввод данных ', 'url_name': 'input_page'},
               {'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'},
               ]
    subsubmenu = [{'title': 'таблица очередность-детали', 'url_name': 'turn'},
                  {'title': 'таблица рейтингов', 'url_name': 'rating'}]
    key = request.session.session_key
    massiv = read_Base(key)
    data = Turn(massiv[0])
    methods = get_methods_from_vocabulary(key)

    data.rating_use(methods, 0)

    new_list = [i for i in data.r2data.keys()]
    tutu = detail_turn_list(data.r2data, key) #НИКОГДА больше так не называй переменные видимо это лист деталей в порядке очереди
    a = []
    for i in range(len(tutu)):
        a.append(new_list[i])

    mydict = dict(zip(tutu, a))

    return render(request, 'interface/turn_another_table.html', {'menu': menu,
                                                                 'sr_num': len(mydict) + 2,
                                                                 'turn3': methods,
                                                                 'det_val': mydict,
                                                                 'submenu': submenu,
                                                                 'submenu2': subsubmenu,
                                                                 'tools_series': list(mydict.values())[0]})


def turn_rating_table(request):
    submenu = [{'title': 'ввод данных ', 'url_name': 'input_page'},
               {'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'},]

    subsubmenu = [{'title': 'таблица очередность-детали', 'url_name': 'turn'},
                  {'title': 'таблица детали-очередность', 'url_name': 'another'}]

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
                                                                'submenu2': subsubmenu,
                                                                'rdata': stec1,
                                                                'r2data': stec2}
                  )


def result(request):

    submenu = [{'title': 'ввод данных ', 'url_name': 'input_page'},
               {'title': 'редактировать сет деталей', 'url_name': 'data_info'},
               {'title': 'выбор параметров эксперимента', 'url_name': 'experiment'}]

    subsubmenu = [{'title': 'таблица очередность-детали', 'url_name': 'turn'},
                  {'title': 'таблица детали-очередность', 'url_name': 'another'},
                  {'title': 'таблица рейтингов', 'url_name': 'rating'}]

    key = request.session.session_key
    massiv = read_Base(key)
    print('massiv',massiv)
    turn_massiv = get_from_base_turn_massiv(key)
    aturn_massiv = copy.deepcopy(turn_massiv)
    series = get_set_from_vocabulary(key)
    method = get_methods_from_vocabulary(key)
    m = start_logic_multi((series[0], series[1]), turn_massiv, series[2])
    a = {}
    turn_det_vocabulary = make_detail_turn_dict(key)

    for i in m:

        a["lvl_" + str(i.lvl)] = {'date': tranformation(turn_det_vocabulary,i.stec),
                                  'firstzero': i.first_nonzero,
                                  'lastnonzero': i.last_nonzero,
                                  'coefficient': calculate_effective_rating(i),
                                  }
    total = 0
    for i in a.values():
        total += i['coefficient']
    total /= len(a)
    total = round(total,2)

    vocabulary = {'details': series[0], 'tools': series[1], 'series': series[2],
                  'methods': get_methods_from_vocabulary(key)}
    a = kill_zero(a)
    max_l = max_length(a)
    return render(request, 'interface/result.html', {'data': json.dumps(a),
                                                     'vocabulary': json.dumps(vocabulary),
                                                     'avocabulary': vocabulary,
                                                     'amassiv': massiv[0],
                                                     'turn_massiv': aturn_massiv,
                                                     'data2': a,
                                                     'menu':menu,
                                                     'submenu': submenu,
                                                     'submenu2': subsubmenu,
                                                     'sum': total,
                                                     'max_l':max_l})


def turn_save(request):
    print('<>' * 50)
    print("VIE turn_save: start ")
    if request.method == "POST":
        key = request.session.session_key
        s = request._post
        comback_urls = {'turn-details': '/turn', 'details-turn': '/turn_another'}
        table_type = s['table']

        print(s)
        s = dict(s)
        print('types', type(s))
        voc_set = get_set_from_vocabulary(key)
        print('table:', s['table'])
        print('turns:', s['turns'])
        valid = validate_save(s, voc_set)
        if False in valid:
            return HttpResponse(f"<a href = '{comback_urls[table_type]}'>Ошибочка , {valid[1]}</a>")
        else:
            set_new_turns(key, s)
            return redirect(f"{comback_urls[table_type]}")


def register_request(request):
    print("авторизация пользователя")
    print(request.user.is_authenticated)
    if request.user.is_authenticated == True:
        return redirect('start_page')

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.data['username']
            password = form.data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend=None)
                messages.success(request, "Registration successful.")
                return redirect("start_page")
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="interface/register.html", context={"register_form": form})


def login_user(request):
    form = AuthenticationForm
    if request.method == "POST":
        password = request.POST['password']
        username = request.POST['username']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("<a href='/'> Регистрация прошла успешно</a>")
        else:
            return HttpResponse("<a href=''>Неправильное имя или пароль</a>")
    return render(request=request, template_name="interface/login.html", context={'form': form})


def logout_user(request):
    logout(request)
    return HttpResponse("<a href='/'> Выход из аккаунта произведен</a>")


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'interface/register2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return list(context.items())


def test_func(request):
    return render(request, 'interface/test.html')


def pass_change(request):
    return render(request, 'interface/change_password.html')