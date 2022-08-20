from django.db.models import Max
from interface.models import *
from django.contrib.sessions.models import Session


"""ТУТ ВСЁ ВЗАИМОДЕЙСТВИЕ С БАЗОЙ ДАННЫХ"""



def read_get_for_experiment(get: dict) -> list:
    "Функция приложение для full_add_to_Base читает запрос и приводит его в нормальную форму"
    a = []
    for key, values in get.items():
        b = [key, values]
        v = b[0].split(',')
        if len(v[0]) <= 3:
            number_of_detail = v[0]
            number_of_stanki = v[1]
            a.append([int(number_of_detail), int(number_of_stanki), b[1]])
    return a


def add_to_Base(mod_get: list, key):
    """Функция приложение для full_add_to_base общается с базой данных"""
    for i in mod_get:
        new = Base()
        a = Session.objects.get(session_key=key)
        new.detail_number = i[0]
        new.detail_stanok_number = i[1]
        new.detail_time = i[2]
        new.redis = a
        new.save()


def del_from_Base_key (key):
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
    пригодный для использования в logic (вычисления)"""

    n = []
    ii = 0
    mn = Base.objects.filter(redis=key).values('detail_time')
    max_details = Base.objects.filter(redis=key).aggregate(Max('detail_number'))['detail_number__max'] + 1
    max_stanki = Base.objects.filter(redis=key).aggregate(Max('detail_stanok_number'))[
                     'detail_stanok_number__max'] + 1
    # print(max_details,max_stanki)
    for i in range(max_details):
        m = []
        for j in range(max_stanki):
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

def read_Base2(key,details):
    """Возвращает лист , порядковых номеров детлей , вытаскивая из базы"""
    detail_list=[]
    for i in range(len(details)):
        print(i,'%'*50)
        detail_list.append(get_from_base(key,i))
    return detail_list



def get_from_base(key,turn):
    a = Base.objects.filter(detail_turn=turn)
    b = a[0].detail_number
    return b



def save_to_vocabulary_sets(sets: int,key: str):
    """ сохраняет в бд Vocabulary колличество серий"""
    a = Session.objects.get(pk=key)
    b = Vocabulary(details=sets[0],tools=sets[1],series=sets[2], redis=a)
    b.save()

def save_to_vocabulary_methods(methods, key):
    """ сохраняет в Vocabulary методы"""
    a = Session.objects.get(pk=key)
    b = Vocabulary.objects.get(redis=a)
    b.methods =','.join(methods)
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

def get_turn_from_base(detail_number: int,key)->int:
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
    stec=[]
    for i in range(num):
        a = Base.objects.filter(detail_turn=i, redis=key)
        ministec = []
        for j in a:
            ministec.append(j.detail_time)
        stec.append(ministec)
    return stec


