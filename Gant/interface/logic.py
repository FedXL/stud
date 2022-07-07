import random

# основной класс
class Data:

    def __init__(self, detail, stanki, p1=0, p2=500, p3=50):
        if self.validate(detail, stanki, p1, p2, p3):
            self.det = detail
            self.st = stanki
            self.a = [[(random.randint(p1, p2) // p3) * p3 for i in range(self.st)] for j in range(self.det)]

    def print_data(self):
        [print(i) for i in self.a]

    def true(self):
        return "123321"

    @classmethod
    def validate(cls, *args, **kwargs):
        for i in args:
            if type(i) != int:
                raise TypeError(f"Введеное значение: {i} в класс Data должны быть integred а не {type(i)}")

        return True



# Много говнокода. простите это функции к трансформации из табличных данных в диаграмму ганта
# запуск realrun на выходе получаете массив ганта.
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
def normilaze1(a,b):

    lvl=0
    stec = massiv_to_stec(a, lvl)
    for i in range(1,b[0]+1):
        change_stec(stec,i,0,lvl)
    stec_to_masiv(a,0,stec)

    return a
def finder(det, stec, placer=0):
    """Функция ищет приемлимую координату для спуска вниз по списку"""
    n1 = 0
    if det in stec:
        n1 = finder_last(det, stec)
        n1 = n1 + 1

    elif det not in stec and det > 1:

        for i in range(det-1, 0,-1):

            n1 = finder_last(i, stec)
            if n1 != 0:
                return n1+1

    if n1 > len(stec)-1:
        n1 = len(stec)-1
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
def change_stec (stec, det, placer,lvl):
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
    stec=[]
    for i in range(len(massiv)):
        stec.append(massiv[i][levl])

    return stec
def stec_to_masiv(massiv, lvl , stec):


    for i in range(len(massiv)):
        massiv[i][lvl] =stec[i]
    return massiv
def normilaze3(massiv,spec_massiv):

    for det in range(2,spec_massiv[0]+1):
        for lvl in range(spec_massiv[1]):
            if lvl==0:
                stec=[]
                for i in range(len(massiv)):
                    stec.append(massiv[i][0])

                down_coords = finder(det, stec)

                if down_coords == 0:
                    for z in range(det, 1, -1):
                        down_coords = finder(z, stec)
                        if down_coords != 0:
                            break
                if down_coords==0 and stec[0]!=0:
                    down_coords=1

            if lvl!=0 and det!=1 and down_coords !="":
                stec = massiv_to_stec(massiv,lvl)
                stec = change_stec(stec, det, down_coords, lvl)
                massiv = stec_to_masiv(massiv, lvl, stec)


            if lvl!=spec_massiv[1]-1  and det !=1:

                x = down_coords

                down_coords = finder(det, stec)

                if down_coords == 0 and x !=0:
                    down_coords = x

    return massiv
def realrun(a:(list,(int,int)))->list:

    AA = a[0]
    BB = (a[1][0], a[1][1])

    A = deliter_zero(AA)
    C = normilaze1(A, BB)
    D = normilaze3(C, BB)
    finaly = []
    for i in D:
        if sum(i) != 0:
            finaly.append(i)
    n = 0
    for i in finaly:
        n += 1
    return finaly

# дополнительные функции:
def massiv_to_stec_massiv(mas:list) -> list:
    """Функция служит для грубо-говоря транспонирования матрицы диаграммы ганта
    для визуализации штмл таблички"""
    new_mass=[]
    for i in range(len(mas[0])):
        new_mass.append(massiv_to_stec(mas,i))
    print(new_mass)
    return new_mass



#запуск и тестирование--------------------------------------

def run(aa,bb):

    new_set = Data(aa,bb)
    AA = new_set.a
    BB = (new_set.det, new_set.st)

    A = deliter_zero(AA)
    C = normilaze1(A,BB)
    D = normilaze3(C,BB)
    finaly=[]
    for i in D:
        if sum(i)!=0:
            finaly.append(i)
    n=0
    for i in finaly:
        n+=1
    return finaly

#тостер 1)-критерий все цифры в стеке (очереди на станок) должны быть возрастающими
def toster(massiv):

    for j in range(len(massiv[0])):
        stec = []
        a = 0
        for i in range(len(massiv)):
            stec.append(massiv[i][j])
        for z in range(len(stec)):
            if stec[z] !=0 and stec[z]>a:
                a = stec[z]
            if stec[z] < a and stec[z] !=0:
                print("Когда это дерьмо кончится",z,j,a,stec[z])
                return False

    print("по первому критерию все окк")
    return True
def supertoster(a,b,c=10):
    for i in range(c):
        d=toster(run(a,b))
        if d == False:
            return print(i,"тест не прошло")
    return print("всё удачно")



#supertoster(10,10,100)
#test_finder(2)

if __name__=="__main__":
    a = run(4,4)
    n=0
    for i in a:
        print("+",n,i)
        n+=1