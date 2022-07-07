from django.db.models import Max
from interface.models import Base

# для BASE читаем get запрос и добавляем таблицу в базу данных
def read_get_for_experiment(get : dict) -> list:
    "Функция приложение для full_add_to_Base читает Get запрос и приводит его в нормальную форму"
    a = []
    print(get)
    for key,values in get.items():
        b = [key,values]
        v = b[0].split(',')
        print(v)
        if len(v[0])<=3:
            print("ding" , v[0],v[1])
            number_of_detail = v[0]
            number_of_stanki = v[1]
            a.append([int(number_of_detail), int(number_of_stanki), b[1]])
    print("-----------------------------------",a)
    return a
def add_to_Base(mod_get:list):
    """Функция приложение для full_add_to_base общается с базой данных"""
    for i in mod_get:
        new = Base()
        new.detail_number=i[0]
        new.detail_stanok_number=i[1]
        new.detail_time=i[2]
        #print("+new",i,new.detail_stanok_number,new.detail_number,new.detail_time)
        new.save()
def clean_Base():
    """очияет Base перед добавлением данных"""
    Base.objects.all().delete()
def full_add_to_Base(get:dict):
    """ Функция для добавления в базу данных информации из редактируемой таблички
    с экспериментальными данными"""
    clean_Base()
    massiv = read_get_for_experiment(get)
    add_to_Base(massiv)

# Функция для доставания информации из Base и превращения этого в массив пригодный для logic

def read_Base() -> (list, (int, int)):
    """Функция считывает данные задачи из базы данных и формирует массив
    пригодный для использования в logic (вычисления)"""
    n=[]
    m=[]
    ii=0
    mn = Base.objects.all().values('detail_time')
    max_details = Base.objects.aggregate(Max('detail_number'))['detail_number__max']+1
    max_stanki = Base.objects.aggregate(Max('detail_stanok_number'))['detail_stanok_number__max']+1
    #print(max_details,max_stanki)
    for i in range(max_details):
        m=[]
        for j in range(max_stanki):
            m.append(mn[ii]['detail_time'])
            ii+=1
        n.append(m)

    return (n,(int(max_details),int(max_stanki)))




