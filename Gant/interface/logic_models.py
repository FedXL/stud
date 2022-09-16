from typing import Tuple, List, Union, Any
from django.db.models import Max
from interface.models import *
from django.contrib.sessions.models import Session

"""ТУТ ВСЁ ВЗАИМОДЕЙСТВИЕ С БАЗОЙ ДАННЫХ"""


def read_get_for_experiment(get: dict) -> tuple[list[list[Union[int, Any]]], Any]:
    "Функция приложение для full_add_to_Base читает запрос и приводит его в нормальную форму"
    a = []
    z = 0
    print("read_get_for....")
    print(get)
    for key, values in get.items():
        b = [key, values]
        v = b[0].split(',')
        z = v
        if len(v[0]) <= 3:
            number_of_detail = v[0]
            number_of_stanki = v[1]
            a.append([int(number_of_detail), int(number_of_stanki), b[1]])
    z[0] = int(z[0]) + 1
    z[1] = int(z[1]) + 1
    return a, z


def add_to_Base(mod_get: list, key):
    """Функция приложение для full_add_to_base общается с базой данных"""
    for i in mod_get[0]:
        new = Base()
        a = Session.objects.get(session_key=key)
        new.detail_number = i[0]
        new.detail_stanok_number = i[1]
        new.detail_time = i[2]
        new.redis = a
        new.save()
    Vocabulary.objects.filter(redis=key).update(details=mod_get[1][0], tools=mod_get[1][1])


def del_from_Base_key(key):
    """Функция для удаления объектов из базы , длея предотвращения их дублирования"""
    try:
        new = Base.objects.filter(redis=key)
        new.delete()
        print('Данные успешно удалены')
    except:
        print('данные не удалены')
        raise Exception('не получилось удалить предыдущий сет из базы данных')


def insert_to_Base():
    pass


def clean_Base():
    """очияет Base перед добавлением данных"""
    Base.objects.all().delete()


def full_add_to_Base(get: dict):
    """ Функция для добавления в базу данных информации из редактируемой таблички
    с экспериментальными данными"""
    clean_Base()
    massiv = read_get_for_experiment(get)
    add_to_Base(massiv)


# Функция для доставания информации из Base и превращения этого в массив пригодный для logic
def read_Base(key: str) -> (list, (int, int)):
    """Функция считывает данные задачи из базы данных и формирует массив
    пригодный для использования в logic (вычисления)
    :key - сессия
    :n - массив из деталей"""

    n = []
    ii = 0
    mn = Base.objects.filter(redis=key).values('detail_time')
    max_details = Base.objects.filter(redis=key).aggregate(Max('detail_number'))['detail_number__max'] + 1
    max_stanki = Base.objects.filter(redis=key).aggregate(Max('detail_stanok_number'))[
                     'detail_stanok_number__max'] + 1
    print(max_details, max_stanki)
    for i in range(max_details):
        m = []
        for j in range(max_stanki):
            print(i, j, ii, mn[ii])
            m.append(mn[ii]['detail_time'])
            ii += 1
        n.append(m)
    return (n, (int(max_details), int(max_stanki)))


def insert_turns_to_base(key: str, detail_list: list):
    """
    Функция для вставки порядковой очереди прохождения деталей на линию
    в Base.

    :param key: Это сессия
    :param detail_list: Это детали в порядке поступления на линию
    :return: не нужен тут ретюрн
    """
    turn = 0
    for i in detail_list:
        pk_list = find_pk(key, i)
        for pk in pk_list:
            insert_turn_to_Base(pk, turn)
        turn += 1


def find_pk(key: str, detail: int) -> list:
    """
    Функция для поиска id  вставляемого элемента.

    :param key: сессия
    :param detail: список деталей в порядке поступления на линию
    :return: Для каждой детали возвращает список из id
    """

    mn = Base.objects.filter(redis=key, detail_number=detail)
    clean_list = []
    for i in mn:
        clean_list.append(i.pk)
    return clean_list


def insert_turn_to_Base(pk: int, turn: int):
    """
    Непосредственно вставляет по id очередь
    :param pk: interface_base id
    :param turn: очередь детали
    :return: не нужен ретюрн
    """

    mn = Base.objects.get(pk=pk)
    mn.detail_turn = turn
    mn.save()


def read_Base2(key, details):
    """Возвращает лист , порядковых номеров детлей , вытаскивая из базы
    это просто прямой порядок номеров деталей
    зачам так сделал непонятно...
    Вероятно мне нужны были ключи к сформированному словорю
    деталей"""
    detail_list = []
    for i in range(len(details)):
        print(i, '%' * 50)
        j = get_from_base(key, i)
        print(j)
        detail_list.append(j)
    return detail_list


def get_from_base(key, turn):
    """:turn это у нас порядковая очередь детали
     :return должно возвращать """
    a = Base.objects.filter(detail_turn=turn, redis=key)
    print(a)
    print('len', len(a))

    b = a[0].detail_number
    return b


def save_to_vocabulary_sets(sets: list, key: str):
    """ сохраняет в бд Vocabulary колличество серий"""
    a = Session.objects.get(pk=key)
    b = Vocabulary(details=sets[0], tools=sets[1], series=sets[2], redis=a)
    b.save()


def save_to_vocabulary_methods(methods, key):
    """ сохраняет в Vocabulary методы"""
    a = Session.objects.get(pk=key)
    b = Vocabulary.objects.get(redis=a)
    b.methods = ','.join(methods)
    b.save()


def get_methods_from_vocabulary(key):
    """ вытаскивает из Vocabulary методы"""
    b = Vocabulary.objects.get(redis=key)
    methods = b.methods.split(',')
    return methods


def get_set_from_vocabulary(key):
    """вытаскивает колличество серий из Vocabulary"""
    b = Vocabulary.objects.get(redis=key)
    set = (b.details, b.tools, b.series)
    return set


def get_turn_from_base(detail_number: int, key) -> int:
    b = Base.objects.filter(detail_number=detail_number, redis=key)
    turn = b[0].detail_turn
    return turn


def detail_turn_list(data, key):
    list_length = len(data)
    turn_list = []
    for i in range(list_length):
        turn_list.append(get_turn_from_base(i, key))
    return turn_list


def get_from_base_turn_massiv(key):
    """возвращает сортированный список деталей"""

    num = get_set_from_vocabulary(key)[0]
    stec = []
    for i in range(num):
        a = Base.objects.filter(detail_turn=i, redis=key)
        ministec = []
        for j in a:
            ministec.append(j.detail_time)
        stec.append(ministec)
    return stec


def set_new_turns(key, queryset):
    """
    Добавляет новые параметры очереди в interface_base
    :param key: сессия
    :param queryset: request.POST из turn_another_table и turn_assert
    :return: без ретюрна
    """

    table_name = queryset['table'][0]
    turns = [int(i) for i in queryset['turns']]
    print("TABLE NAME:", table_name)

    if table_name == 'turn-details':
        details = [int(i) for i in queryset['details']]
        for i in range(len(details)):
            a = Base.objects.filter(detail_number=details[i], redis=key)
            a.update(detail_turn=turns[i])
            print("ПОЛУЧИЛОСЬ-1")
    elif table_name == 'details-turn':
        for i in range(len(turns)):
            a = Base.objects.filter(detail_number=i, redis=key)
            a.update(detail_turn=turns[i])
            print("ПОЛУЧИЛОСЬ-2")
    else:
        raise Exception("Some problem with queryset or Base")


def make_detail_turn_dict(key: str) -> dict:
    """
    :param key: session
    :return: dict { turn : detail number }
    """

    block = Base.objects.filter(redis=key)
    turn_det_vocabulary = {0: 0}
    for i in block:
        turn_det_vocabulary[i.detail_turn + 1] = i.detail_number + 1
    return turn_det_vocabulary


def tranformation(vocabulary, stec):
    """перебирает входящий список-стек очередей и в соответсвии со словарём
    формирует список-стек деталей для result """
    new_stec = [vocabulary[i] for i in stec]
    return new_stec


def kill_zero(a):
    """убирает хвостик из нулей из первого стека
    (стек для построения картинки диаграммы)"""
    x = a['lvl_0']['date']
    print(type(x))
    print(x)
    kill_index = x.index(0)
    xx = x[:kill_index]
    print(xx)
    a['lvl_0']['date'] = xx
    return a


def max_length(a):
    """находит максимально длинный кусок стека
    для выравнивания окна canvas в result.html"""
    maxl, new_max = 0, 0

    for i in a.values():
        maxl = len(i['date'])
        if maxl > new_max:
            new_max = maxl
    return new_max


def add_to_archive(request):
    """ Сохраняет эксперимент в архив"""
    key = request.session.session_key
    user_pk = request.user.pk
    user = User.objects.get(pk=user_pk)

    methods = request.POST['method']
    coefficient = request.POST['coeff']
    exp = request.POST['explain']

    voc = Vocabulary.objects.get(pk=key)

    archive_str = ArchiveLetter(explain=exp,
                                method=methods,
                                rating=coefficient,
                                name=user,
                                details=voc.details,
                                tools=voc.tools,
                                series=voc.series)
    archive_str.save()

    a = Base.objects.filter(redis=key)

    for i in a:
        d = ArchiveData(detail_number=i.detail_number,
                        detail_tools_number=i.detail_stanok_number,
                        detail_time=i.detail_time,
                        record_number=archive_str)
        d.save()


def get_from_archive(request):
    """Вытаскивает из архива данные и прерващает их в контекст
    Из реквестав берёт юзера"""
    print("get_from_archive: start")
    user_pk = request.user.pk
    user = User.objects.get(pk=user_pk)
    d = ArchiveLetter.objects.filter(name=user)
    context = []

    for i in d.values():
        j = ArchiveData.objects.filter(record_number=i['id'])
        z = j.values()
        make_list = i['method']
        make_list = make_list.replace('[', '')
        make_list = make_list.replace(']', '')
        make_list = make_list.replace("'", "")
        make_list = make_list.replace(" ", "")
        make_list = make_list.split(',')
        i['method'] = make_list
        stec2 = stec_returner(z)
        i['data'] = stec2
        print(i.get('data'))
        context.append(i)

    return context


def stec_returner(a: list) -> tuple:
    """utils for get_from_archive"""
    print('start func: stec_returner', "*" * 50)
    big_stec = []
    stec = []

    for i in a:
        x = i['detail_tools_number']
        if x == 0:
            if len(stec) > 0:
                big_stec.append(tuple(stec))
            stec = []
        stec.append(i['detail_time'])
    big_stec.append(tuple(stec))
    print(big_stec)
    print('stec_returner: end func' )
    return big_stec

def del_records_from_archive(request):
    id = request.GET.get('record_id')
    a = ArchiveLetter.objects.get(id=id)
    a.delete()