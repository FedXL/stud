import random
from dataclasses import dataclass
from random import sample

class Data:
    """генератор, заполнитель случайных значений для начала эксперимента"""

    def __init__(self, detail, stanki, p1=0, p2=500, p3=50):
        if self.validate(detail, stanki, p1, p2, p3):
            self.det = detail
            self.st = stanki
            self.a = [[(random.randint(p1, p2) // p3) * p3 for i in range(self.st)] for j in range(self.det)]

    def print_data(self):
        [print(i) for i in self.a]

    @classmethod
    def validate(cls, *args, **kwargs):
        for i in args:
            if type(i) != int:
                raise TypeError(f"Введеное значение: {i} в класс Data должны быть integred а не {type(i)}")
        return True


# Много говнокода. простите но общий смысл из таблички [[50,50,50],......]
# Сделать ряды, пригодные для рисования диаграмм ганта.

def check_step(b=None):
    if b is None:
        b = [1, 2, 3]
    a = 0
    for i in b:
        a += i
    if a == 0:
        return False
    else:
        return True


def date_return(a, step):
    m, n = 0, 0
    x = 1  # переменная номера детали
    timer = 0
    task_matrix = [[0 for _ in range(len(a[0]))]]
    for detail in a:
        # detail [ 5,10,20..n]
        while check_step(detail):
            if detail[n] != 0:
                detail[n] -= step
                task_matrix[m][n] = x  # То что будет написано в матрице
                timer += step
            else:
                n += 1
            task_matrix.append([0 for _ in range(len(detail))])
            m += 1
        x += 1
        n = 0
    return task_matrix


def deliter_zero(a):
    A = []
    for i in date_return(a, 50):
        if sum(i) != 0:
            A.append(i)
    return A


def normilaze1(a, b):
    lvl = 0
    stec = massiv_to_stec(a, lvl)
    for i in range(1, b[0] + 1):
        change_stec(stec, i, 0, lvl)
    stec_to_masiv(a, 0, stec)
    return a


def finder(det, stec, placer=0):
    """Функция ищет приемлимую координату для спуска вниз по списку"""
    n1 = 0
    if det in stec:
        n1 = finder_last(det, stec)
        n1 = n1 + 1
    elif det not in stec and det > 1:
        for i in range(det - 1, 0, -1):
            n1 = finder_last(i, stec)
            if n1 != 0:
                return n1 + 1

    if n1 > len(stec) - 1:
        n1 = len(stec) - 1
    return n1


def finder_last(det, stec):
    """Функция служит для определения координаты последней детали в стеке
    стек формируется из одной линии списка ( считай линия одного станка) внутренняя функция для founder"""
    n = 0
    ni = 0
    dcopy = [item for item in stec]
    for i in dcopy:

        if i == det:
            dcopy[n] = "хуй"
            ni = n
        n += 1
    return ni


def change_stec(stec, det, placer, lvl):
    """ функция для перестановки стека
    """

    det_i = None
    if det == 1:
        return stec

    while True:
        if placer >= len(stec):
            break
        if stec[placer] != 0:
            placer += 1
            continue
        if stec[placer] == 0:
            for i in range(placer, len(stec)):
                if stec[i] == det:
                    det_i = i
                    break
                else:
                    det_i = None

        if stec[placer] == 0 and det_i is not None:
            stec[placer] = det
            stec[det_i] = 0
        else:
            break
    return stec


def massiv_to_stec(massiv, levl):
    stec = []
    for i in range(len(massiv)):
        stec.append(massiv[i][levl])

    return stec


def stec_to_masiv(massiv, lvl, stec):
    for i in range(len(massiv)):
        massiv[i][lvl] = stec[i]
    return massiv


def normilaze3(massiv, spec_massiv):
    for det in range(2, spec_massiv[0] + 1):
        for lvl in range(spec_massiv[1]):
            if lvl == 0:
                stec = []
                for i in range(len(massiv)):
                    stec.append(massiv[i][0])

                down_coords = finder(det, stec)

                if down_coords == 0:
                    for z in range(det, 1, -1):
                        down_coords = finder(z, stec)
                        if down_coords != 0:
                            break
                if down_coords == 0 and stec[0] != 0:
                    down_coords = 1

            if lvl != 0 and det != 1 and down_coords != "":
                stec = massiv_to_stec(massiv, lvl)
                stec = change_stec(stec, det, down_coords, lvl)
                massiv = stec_to_masiv(massiv, lvl, stec)

            if lvl != spec_massiv[1] - 1 and det != 1:

                x = down_coords
                down_coords = finder(det, stec)
                if down_coords == 0 and x != 0:
                    down_coords = x

    return massiv


# запуск
def run(sets, details_set):
    AA = details_set
    #BB = (new_set.det, new_set.st)
    BB = (sets[0], sets[1])

    A = deliter_zero(AA)
    C = normilaze1(A, BB)
    D = normilaze3(C, BB)
    finaly = []
    for i in D:
        if sum(i) != 0:
            finaly.append(i)
    n = 0
    for i in finaly:
        print(n, i)
        n += 1
    return finaly


# тут я еще не знал про Pytest по этому тестировал как мог...
# тостер 1)-критерий все цифры в стеке (очереди на станок) должны быть возрастающими

def toster(massiv):
    for j in range(len(massiv[0])):
        stec = []
        a = 0
        for i in range(len(massiv)):
            stec.append(massiv[i][j])
        for z in range(len(stec)):
            if stec[z] != 0 and stec[z] > a:
                a = stec[z]
            if stec[z] < a and stec[z] != 0:
                print("Когда это дерьмо кончится", z, j, a, stec[z])
                return False

    print("по первому критерию все окк")
    return True


def supertoster(a, b, c=10):
    for i in range(c):
        d = toster(run(a, b))
        if d == False:
            return print(i, "тест не прошло")
    return print("всё удачно")


# дальше много страданий, для реализации фитчи "партии", грубо говоря
# Умножитель матрицы для построения диаграмм ганта.
# Ну а потом я подумал, что использовать конструкцию Датаклассов для построения
# диаграмм удобнее. И в воообще строчными масивами оперировать удобнее.

@dataclass
class Stec:
    """конструкция для хранения и манипуляциями срезами"""
    stec: list  # срез по уровням из основного массива
    lvl: int = 0  # Уровень стека
    incision: int = 0  # Индекс стека где происходит склейка
    first_nonzero: int = 0  # Индекс первого ненулевого элемента в стеке
    last_nonzero: int = 0  # Индекс последнего ненулевого элемента в стеке
    max: int = 0  # максимальный номер детали в стеке
    min: int = 0  # минимальный номер детали в стеке


# --------- функции для наполнения Stec информацией и формирования massiv:


def make_stecclass(massiv: list) -> list:
    """служит для наполнения конструкции
    [Stec1,Stec2,...,StecN]
    параметрами
    параметр turn down тут не расчитывается"""
    m = []
    for i in range(len(massiv[0])):
        stec = []
        for j in range(len(massiv)):
            stec.append(massiv[j][i])
        maxi = max(stec)
        nonzero = first_nonzero(stec, maxi)
        mini = find_min_element(stec, maxi)
        nonzero2 = finder_last(maxi, stec)
        if maxi == 0:
            nonzero2 = 0
        m.append(Stec(stec, i, 0, nonzero, nonzero2, maxi, mini))
    return m


def first_nonzero(stec: list, max: int) -> int:
    """вспомогательная функция для make_stecclass
    находит индекс первого не нулевого элемента
    если их нет , возвращает 9999"""
    n = 0
    while n <= max:
        n += 1
        if n in stec:
            nonzero = stec.index(n)
            return nonzero
    return 9999


def find_min_element(stec: list, max: int) -> int:
    """вспомогательная функция для make_stecclass
    находит минимальный элемент в стеке.
    Если элементов нет , возвращает 9999"""
    n = 0
    while n <= max:
        n += 1
        if n in stec:
            return n
    return 9999


# две функции для мультиплицирования текущего стека
# first_line для удлиннения massiv[0] первой линии массива
# line_next для удлиннения massiv[i] остальных линий массива

def first_line(stec_class: list):
    """ Функция для увеличения верхнего стека массива (по упрощеной схеме)"""
    print("start first line")
    m = stec_class[0]
    stecc = m.stec
    ni = m.last_nonzero + 1
    if m.incision == 0:
        nj = m.first_nonzero
    else:
        nj = m.incision
    stecc = stecc[:ni] + stecc[nj:]
    m.stec = stecc
    m.incision = ni
    m.last_nonzero = finder_last(m.max, stecc)
    print("stop firts line")


def line_next(stec_class: list):
    print("line_next_start_" * 20)
    maxdetail = 0
    for i in stec_class:
        big = max(i.stec)
        if maxdetail < big:
            maxdetail = big
    for i in range(1, len(stec_class)):
        memory_incision = stec_class[i].last_nonzero + 1
        for j in range(1, maxdetail + 1):
            print("<<<", "start new iteration", i, j, "уровень/деталь", ">>>")
            if j in stec_class[i].stec:
                down_coords = coordinates_to_down(i, j, stec_class)
                ministec = stec_slicer(i, j, stec_class)
                print("срез", stec_class[i].incision)
                maxistec = stec_preparing(i, j, down_coords, stec_class)
                newstec = maxistec + ministec
                stec_class[i].stec = newstec
                stec_class[i].last_nonzero = finder_last(j, newstec)
                print("это новый стек", newstec)
            else:
                print("нет детали нет проблемы")

        stec_class[i].incision = memory_incision
        stec_class[i].last_nonzero = finder_last(stec_class[i].max, stec_class[i].stec)
    print("line_next_finish_" * 20)


# вспомогательные функции для line_next:

def stec_preparing(i: int, j: int, downcoords, stec_class: list) -> list:
    """Функция готовит стек для слияния с министеком"""
    if downcoords <= stec_class[i].last_nonzero + 1:
        insert_coords = stec_class[i].last_nonzero + 1
        maxistec = stec_class[i].stec[:insert_coords]
        return maxistec
    elif downcoords > stec_class[i].last_nonzero + 1:
        zerostec = (downcoords - stec_class[i].last_nonzero - 1) * [0]
        insert_coords = stec_class[i].last_nonzero + 1
        maxistec = stec_class[i].stec[:insert_coords]
        newmaxistec = maxistec + zerostec
        return newmaxistec


def stec_slicer(i: int, j: int, stec_class: list) -> list:
    """Вернуть кусочек среза который нужно будет присовокупить к текущему стеку"""
    assert j in stec_class[i].stec, "Деталь должна быть в стеке"
    print("start stec_slicer:", i, j)
    coord_to_find = stec_class[i].incision
    print(coord_to_find)
    stec = stec_class[i].stec[coord_to_find:]
    print(stec)

    x_coord = stec.index(j)
    y_coord = finder_last(j, stec)
    print("кусочек", stec[x_coord:y_coord + 1])
    return stec[x_coord:y_coord + 1]


def coordinates_to_down(lvl: int, detail: int, massiv: list) -> int:
    """функция ищет минимально возможную координату для спуска по каждой детали.
    Если детали нет возвращает координату начала склейки"""

    print("coordinates_to_down: start")
    lvl_search = find_lvl(lvl, detail, massiv)
    if lvl_search == "zero":
        print("cooordingates_to_dawin: обработка False")
        print("coordinates_to_down coord:", massiv[0].incision)
        return massiv[0].incision

    coords = finder_last(detail, massiv[lvl_search].stec) + 1
    print("coordinates_to_down: ", coords, " finish")
    return coords


def find_lvl(lvl_income, detail, massiv):
    """Функция для поиска уровня , в котором искать спуск"""
    i = lvl_income
    while i > 0:
        i -= 1
        if detail in (massiv[i].stec):
            print("find_lvl: ", i, "нашли уровень с деталью")
            return i
    print("find_lvl: Такой детали в верхних уровнях нет")
    print("find_lvl: return: Zero")
    return "zero"


# Ну и функция для запуска всего этого безобразия


def start_logic_multi(tools: tuple[int, int], details: list, iteration=1):
    """ Функция для исполнения. Именно эту функцию нужно использовать
    для старта всего модуля логики
    :sets: это параметры сета из деталей (детали,станки)
    :details: сет из деталей"""

    assert iteration >= 1 or iteration == int, " неправильное значение итераций  "
    iteration -= 1
    mas = run(tools, details)
    m = make_stecclass(mas)
    if iteration < 1:
        return m
    for i in range(iteration):
        print("i" * 50, i)
        first_line(m)
        line_next(m)
    return m

def calculate_effective_rating(stec)-> float:
    """
    Функция для расcчета коэффициента загруженности станков
    :param stec: датакласс Stec
    :return: коэфициент загруженности станков
    """

    devider = stec.last_nonzero +1 - stec.first_nonzero
    numerator = stec.stec[stec.first_nonzero:stec.last_nonzero].count(0)
    result = 100 - (numerator/devider)*100
    result=round(result,2)
    return result

def calculate_effective_rating_sum(a_dict:dict)->float:
    sum = 0
    b = a_dict.values()
    print(b)
    b = dict(b)
    for i in b:
        sum += i['corfficient']
    rating = sum/len(a_dict)
    rating =round(rating,2)
    return rating


@dataclass
class Detail:
    """
    Structure to container detail info
    """
    index: int
    body: tuple


class Turn:
    """
    Класс для Управления системой рейтинга.
    каждая функция : spt, ltp, lukr, mwkr, fopnr, antifopnr
    меняет порядок подачи деталей и возвращает порядок деталей соответсвии
    с правилами.

    random возвращает случайный порядок

    функция rating_returner собирает рейтинг для деталей для каждого из правил.
    """
    settings = {
        "spt": 1,
        "ltp": 1,
        'lukr': 1,
        'mwkr': 1,
        'fopnr': 1,
        'antifopnr': 1
    }

    def __init__(self, data):
        data = self.data_mod(data)
        self.data = [tuple(i) for i in data]
        self.altdata = [Detail(i, (self.data[i])) for i in range(len(self.data))]
        self.rdata = {i: {"spt": int, "ltp": int, "lukr": int, "mwkr": int, "fopnr": int, "antifopnr": int}
                      for i in range(len(self.data))}
        self.r2data = {self.data[i]: i for i in range(len(self.data))}
        # формирование rdata, составление таблицы рейтинга для каждой детали по всем методам:

        self.spt(2)  # любое значение в методе отличное от нуля не переставляет детали местами.
        self.ltp(2)
        self.lukr(2)
        self.mwkr(2)
        self.fopnr(2)
        self.antifopnr(2)

        self.rating_settings()  # вес рейтинга

    @staticmethod
    def data_mod(data):
        print("strart data_mod")
        i = 0
        print(data)
        while True:
            count = data.count(data[i])
            print("count", count)
            if count > 1:
                j = data.index(data[i], i + 1)
                st = data[j]
                print(st)
                print(len(st))
                data[j][len(st) - 1] += 0.000001
                continue
            i += 1
            print(i, "Новая итерация", data)
            if i == len(data):
                break
        return data

    def rating_settings(self):
        """Утанавливает вес рейтинков, умножает каждый рейтинг на его вес.
        вес зашит в cls класса"""

        for method, settings in self.settings.items():
            for rating_value in self.rdata.values():
                rating_value[method] *= settings

    def rating_returner(self, new_data, name):
        n = len(new_data)
        print(f"***{name} start rating_returner")
        print(self.r2data)
        print(self.rdata)
        for i in range(len(new_data)):
            a = self.r2data[new_data[i]], n
            self.rdata[a[0]][name] = a[1]
            n -= 1
        for i, j in self.rdata.items():
            print("<<<>>> rating_returner:", name, j[name])
        assert len(self.rdata) == len(self.r2data)

    @staticmethod
    def rating_fraud(number, minus):
        """
        Функция для модифицирования первичного рейтинга.
        дело в том, что все методы : spt,ltp и дт работают на сравнении словарей
        ключами словаря , же служит рейтинг. А он бывает одинаковым. Вот и приходится мухлевать,
        что бы избежать коллизий пи формировании словаря
        """

        if not minus:
            if number != 0:
                number += number / 250
            else:
                number += 1 / 250
            return number
        if minus:
            if number != 0:
                number -= number / 250
            else:
                number -= 1 / 250
            return number

    @staticmethod
    def get_rating_dict(self, rating: list, minus=False) -> {int: {}}:
        """
       return: Возвращает рейтинг

       minus = False коллизия с одинаковым рейтингом в словаре разрешается
       прибавлением небольшого числа к ключу.

       minus = True коллизия из-за одинакового рейтинга в словаре рейтинга разрешается
       вычитанием небольшого числа от ключа
        """
        rating_dict = {}
        new = 0
        end = len(self.data)
        while True:
            i = new
            if rating[i] not in rating_dict:
                rating_dict[rating[i]] = self.data[i]
            else:
                rating[i] = self.rating_fraud(rating[i], minus)
                new = i
                continue
            i += 1
            new = i
            if i == end:
                break
        return rating_dict

    @staticmethod
    def foo_for_spt(num):
        """функция для метода spt из float 150.00001 делает Str (15000001)"""
        if type(num) == float:
            num = str(num)
            num = num.split(".")
            num = "".join(num)
            return num
        else:
            return num

    def operator(self, i):
        """функция для формирования рейтинка в spt и ант и ltp"""
        operan = {
            50 > i >= 0 and type(i) == int: "000",
            100 > i >= 50 and type(i) == int: "050",
            i >= 100 and type(i) == int: str(i),
            type(i) == float: self.foo_for_spt(i)
        }
        return operan[True]

    def spt(self, changer=0):
        """Если время обработки детали на данной операции минимально,
         то эта деталь обрабатывается в первую очередь"""
        print("*" * 50)
        print("SPT data before:", self.data)
        print("SPT rdata r2data:")
        print(self.rdata)
        print(self.r2data)
        print(self.data)

        pre_rating = [[self.operator(i) for i in j] for j in self.data]
        print("pre_rating", pre_rating)
        rating = [float('1.' + ''.join(i)) for i in pre_rating]
        print("pre_rating", rating)
        rating_dict = self.get_rating_dict(self, rating)
        assert len(rating_dict) == len(self.data), "коллизия в создании словаря"
        print('------>>>>>>>>>>>>>>>>>>>>>>>>>>', rating)
        print('rating_dict', rating_dict)
        another_rating = rating[:]
        another_rating.sort()
        another_data = [(rating_dict[i]) for i in another_rating]
        print("SPT another_data:", another_data)
        name = "spt"
        self.rating_returner(another_data, name)
        if changer == 0:
            self.data = another_data
        print("SPT data after:", self.data)
        print("*" * 50)

    def ltp(self, changer=0):
        """longest progressing time - Если время обработки детали на данной
        операции максимально, то эта деталь обрабатывается в первую очередь"""
        name = 'ltp'
        print("*" * 50)
        print("LTP data before:", self.data)
        pre_rating = [[self.operator(i) for i in j] for j in self.data]
        rating = [float('1.' + ''.join(i)) for i in pre_rating]
        print('------>>>>>>>>>>>>>>>>>>>>>>>>>>', rating)
        rating_dict = self.get_rating_dict(self, rating)
        assert len(rating_dict) == len(self.data), "коллизия в создании словаря"
        another_rating = rating[:]
        another_rating.sort()
        another_rating.reverse()
        another_data = [(rating_dict[i]) for i in another_rating]
        self.rating_returner(another_data, name)
        if changer == 0:
            self.data = another_data
        print("LTP data after:", self.data)
        print("*" * 50)

    def lukr(self, changer=0):
        """Выбор работы, для которой длительность всех оставшихся операций минимальна
        если деталь """
        name = 'lukr'
        print("*" * 50)
        print("lukr data before:", self.data)
        rating = [sum(i) for i in self.data]
        print('------>>>>>>>>>>>>>>>>>>>>>>>>>>', rating)
        rating_dict = self.get_rating_dict(self, rating)
        assert len(rating_dict) == len(self.data), "коллизия в создании словаря"
        print("rating_dict:", rating_dict)
        another_rating = rating[:]
        another_rating.sort()
        another_rating.reverse()
        print("another_rating: ", another_rating)
        another_data = [(rating_dict[i]) for i in another_rating]
        print("another_data: ", another_data)
        self.rating_returner(another_data, name)
        if changer == 0:
            self.data = another_data
        print("lukr data after:", self.data)
        print("*" * 50)

    def mwkr(self, changer=0):
        """Выбор детали , для которой длительность оставшихся операций максимальна.
        Если у данной детали длительность всех невыполненных операций максимальна , то
        она обрабатывается первой"""
        print("*" * 50)
        name = 'mwkr'
        print("mwkr data before: ", self.data)
        rating = [sum(i) for i in self.data]
        print('------>>>>>>>>>>>>>>>>>>>>>>>>>>', rating)
        rating_dict = self.get_rating_dict(self, rating)
        assert len(rating_dict) == len(self.data), "коллизия в создании словаря"
        another_rating = rating[:]
        another_rating.sort()
        print("another_rating:", another_rating)
        another_data = [(rating_dict[i]) for i in another_rating]
        print("another_data:", another_data)
        self.rating_returner(another_data, name)
        if changer == 0:
            self.data = another_data
        print("mwkr data after: ", self.data)
        print("*" * 50)

    def fopnr(self, changer=0):
        """Выбор детали по минимальному колличеству оставшихся к выполнению операций"""
        print("*" * 50)
        name = 'fopnr'
        print("fopnr data before:", self.data)
        rating = [[0 if i == 0 else 1 for i in j] for j in self.data]
        rating = [str(sum(i)) for i in rating]
        print('------>>>>>>>>>>>>>>>>>>>>>>>>>>', rating)

        for i in range(len(rating)):
            rating[i] += "." + str(i)
            rating[i] = float(rating[i])

        rating_dict = self.get_rating_dict(self, rating)
        assert len(rating_dict) == len(self.data), "коллизия в создании словаря"
        another_rating = rating[:]
        another_rating.sort()
        print("another_rating:", another_rating)
        another_data = [(rating_dict[i]) for i in another_rating]
        self.rating_returner(another_data, name)
        if changer == 0:
            self.data = another_data
        print("fopnr data before:", self.data)
        print("*" * 50)

    def antifopnr(self, changer=0):
        """ Выбор детали по максимальному колличеству оставшихся итераций """
        name = 'antifopnr'
        print("*" * 50)
        print("antifopnr data before: ", self.data)
        rating = [[0 if i == 0 else 1 for i in j] for j in self.data]
        rating = [str(sum(i)) for i in rating]
        print('------>>>>>>>>>>>>>>>>>>>>>>>>>>', rating)

        for i in range(len(rating)):
            rating[i] += "." + str(i)
            rating[i] = float(rating[i])

        rating_dict = self.get_rating_dict(self, rating)
        assert len(rating_dict) == len(self.data), "коллизия в создании словаря"
        another_rating = rating[:]
        another_rating.sort()
        another_rating.reverse()
        another_data = [(rating_dict[i]) for i in another_rating]
        self.rating_returner(another_data, name)
        if changer == 0:
            self.data = another_data
        print("antifopnr data after: ", self.data)
        print("*" * 50)

    def random(self, changer=0):
        """устанавливает случайный порядок деталей """
        name = 'random'
        print("*" * 50)
        print(f"{name} data before:", self.data)
        new = sample(self.data, len(self.data))
        self.data = new

        print(f"{name} data after:", self.data)
        print("*" * 50)

    def rating_use(self, methods: list, changer=0):
        """
        Функция для перестановки self.data в соответствии с таблицей рейтинга

        param methods: сюда загружаются правила по которомым будет учитыватся система рейтингов
        пары (spt,ltp),('lukr,mwkr'),(fopnr,antifopnr) имеют взаимообратный рейтинг,
        их суммарный рейтинг всегда = const, пр этому использование пары вместе при
        одинаковых settings бессмыслено.

        param changer: если не ноль , то изменения в self.data НЕ зафиксируются.
        изначально используется в конструкторе класса с параметром не ноль, для
        формирования таблицы рейтингов.
        return:
        """

        if 'random' in methods:
            self.random()
            return

        sum_name = "sum"
        sum_stec = []
        for j in self.rdata.values():
            sum = 0
            for method in methods:
                sum += j[method]
            sum_stec.append(sum)
            j[sum_name] = sum

        rating_dict = self.get_rating_dict(self, sum_stec, minus=True)
        print(rating_dict)
        another_rating = sum_stec[:]
        another_rating.sort(reverse=True)
        print(another_rating)
        new_data = []
        for i in another_rating:
            new_data.append(rating_dict[i])
        print(new_data)
        if changer == 0:
            self.data = new_data


# *********************************************************************
# SPECIAL HELPING FUNC FOR VIEWS:
# *********************************************************************


def check_request(queryset: dict)-> list:
    """
    Функция для вытаскивания из реквест запроса списка методов-правил,
    для определения очереди поставки деталей на конвеер
    :param queryset: приходит из реквеста
    :return: возвращает набор  правил для работы сортировочного класса Turn
    """

    checklist = ['spt+ltp', 'lukr+mwkr', 'fopnr+anti', 'random']
    newlist = [i for i in checklist if i in queryset]
    if not newlist:
        newlist = "make choice again"
        return newlist

    backlist = [queryset[i] for i in newlist]
    return backlist

def  del_list_methods(methods):
    base_list=['spt','ltp','lukr','mwkr','fopnr','antifopnr']
    return list(set(base_list)-set(methods))


def rating_table_list(methods,date):
    kill_methods = del_list_methods(methods)
    for i in kill_methods:
        for j in date.values():
            del j[i]
    return date


def validate_input(s):
    details = int(s['st1'])
    tools = int(s['st2'])
    series = int(s['st3'])

    message = "all right"

    if 50*50*2 > details*tools*series > 25*25*2:
        message = f"Упс! Вы хотите слишком многого." \
                  f"Сумма сета-{details*tools*series} и она превышает" \
                  f" 25*25*2 ,скорее всего на финальной стадии эксперимента ничего" \
                  f"не получится. Вам точно нужно так много?"
        return True, message

    elif details*tools*series > 50*50*2:
        message = f"Упс! Вы хотите очень многого." \
                  f"Сумма сета - {details*tools*series},<br>" \
                  f"что превышает все мыслимые и немыслимые значения. <br>" \
                  f"Я отказываюсь это считать!"
        return None, message
    else:
        return True, message

def validate_save(s:dict, voc_set:(int,int,int))->(bool, str):
    """Функция для проверки валидности значений формы (Детали-очередь)
    и (Очередь-Детали)

    s - request.POST
    set - из vocabulary параметры (детали,станки,серии)
    """
    print("validate_save: start")
    name = s['table']
    post_set = s['turns']
    print('post_set', post_set)
    turn_set = [int(turn) for turn in post_set]
    details = voc_set[0]
    print("details:", details)
    message = "All Right"
    print("name:", name)

    if len(set(turn_set)) != details:
        message = "Двум деталям присвоена одна очередь"
        return False, message
    if max(turn_set) != details-1:
        message = "Одно из значений в очереди превышает колличество деталей"
        return False, message
    elif min(turn_set) != 0:
        message = "Одно из значений в очерeди отрицательное"
        return False, message
    return True, message






