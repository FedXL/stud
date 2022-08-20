import pytest
from dataclasses import dataclass
from logic import find_lvl, coordinates_to_down, stec_slicer, stec_preparing,Turn


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


a1 = Stec([1,1,1,1,2,2,2,2,4,4,2,1,1,1,1,2,2,2,2,4,4,4],
          0,11,0,21,4,1)
a2 = Stec([0,0,0,0,1,1,1,3,3,3,3,4],
          1,0,4,11,1,4)
a3 = Stec([0,0,0,0,0,0,0,1,0,0,0,3],
          2,0,7,11,1,3)

massiv = [a1,a2,a3]

@pytest.mark.parametrize("a,b,result",[
                                (1,3,'zero'),
                                (1,2,0),
                                (1,4,0),
                                (2,2,0),
                                (2,3,1),
                                (2,4,1)])

def test_lvl_search_multi(a,b,result):
    assert find_lvl(a, b, massiv) == result

def test_down_coord():
    assert coordinates_to_down(1,2,massiv) == 19

def test_down_coord2():
    assert coordinates_to_down(1,4,massiv) == 22


@pytest.mark.parametrize("a,b,result",[
                                (1,1,[1,1,1]),
                                (1,3,[3,3,3,3]),
                                (1,4,[4]),
                                (2,1,[1]),
                                (2,3,[3])])
def test_slicer(a,b,result):
    assert stec_slicer(a,b,massiv) == result
@pytest.mark.parametrize("a,b,downcoord,result",[
    (1, 1, 15, [0,0,0,0,1,1,1,3,3,3,3,4,0,0,0]),
    (2, 1, 18, [0,0,0,0,0,0,0,1,0,0,0,3,0,0,0,0,0,0]),
    (2, 1, 5, [0,0,0,0,0,0,0,1,0,0,0,3])
])
def test_stec_peparing(a,b, downcoord,result):
    assert stec_preparing(a, b, downcoord, massiv) == result



mas1 = [[300, 450, 0], [400, 100, 150], [200, 200, 250]]
mas2 = [[150, 450, 0], [300, 0, 150], [300, 0, 150]]
mas4 = [[150, 450, 0], [300, 0, 150], [300, 0, 150], [300, 0, 150],[300, 0, 150]]
mas5 = [[50, 450, 100], [250, 0, 150], [0, 250, 200]]

answer1 = {0: {'spt': 2, 'ltp': 2, 'lukr': 3, 'mwkr': 1, 'fopnr': 3, 'antifopnr': 1},
           1: {'spt': 1, 'ltp': 3, 'lukr': 1, 'mwkr': 3, 'fopnr': 2, 'antifopnr': 2},
           2: {'spt': 3, 'ltp': 1, 'lukr': 2, 'mwkr': 2, 'fopnr': 1, 'antifopnr': 3}}

answer2 = {0: {'spt': 3, 'ltp': 1, 'lukr': 3, 'mwkr': 1, 'fopnr': 3, 'antifopnr': 1},
           1: {'spt': 2, 'ltp': 2, 'lukr': 1, 'mwkr': 3, 'fopnr': 2, 'antifopnr': 2},
           2: {'spt': 1, 'ltp': 3, 'lukr': 2, 'mwkr': 2, 'fopnr': 1, 'antifopnr': 3}}

answer4 = {0: {'spt': 5, 'ltp': 1, 'lukr': 5, 'mwkr': 1, 'fopnr': 5, 'antifopnr': 1},
           1: {'spt': 4, 'ltp': 2, 'lukr': 1, 'mwkr': 5, 'fopnr': 4, 'antifopnr': 2},
           2: {'spt': 3, 'ltp': 3, 'lukr': 2, 'mwkr': 4, 'fopnr': 3, 'antifopnr': 3},
           3: {'spt': 2, 'ltp': 4, 'lukr': 3, 'mwkr': 3, 'fopnr': 2, 'antifopnr': 4},
           4: {'spt': 1, 'ltp': 5, 'lukr': 4, 'mwkr': 2, 'fopnr': 1, 'antifopnr': 5}}

answer5 ={0: {'spt': 2, 'ltp': 2, 'lukr': 3, 'mwkr': 1, 'fopnr': 1, 'antifopnr': 3},
          1: {'spt': 1, 'ltp': 3, 'lukr': 1, 'mwkr': 3, 'fopnr': 3, 'antifopnr': 1},
          2: {'spt': 3, 'ltp': 1, 'lukr': 2, 'mwkr': 2, 'fopnr': 2, 'antifopnr': 2}}


@pytest.mark.parametrize("a,result",[
                                (mas1,answer1),
                                (mas2,answer2),
                                (mas4,answer4),
                                (mas5,answer5)
])

def test_lvl_search_multi(a,result):
    resa  = Turn(a)
    assert resa.rdata == result

test4=[[400, 450, 100, 150, 450, 400, 0, 0, 350, 200], [200, 200, 0, 50, 50, 50, 100, 0, 350, 250], [450, 450, 0, 250, 150, 350, 0, 200, 150, 400], [450, 200, 250, 350, 300, 400, 50, 50, 0, 100], [50, 450, 150, 250, 300, 100, 0, 200, 150, 300], [400, 100, 250, 200, 100, 400, 300, 150, 300, 0], [350, 200, 50, 300, 350, 200, 150, 350, 0, 200], [50, 150, 400, 150, 450, 0, 200, 100, 400, 100], [400, 350, 450, 450, 250, 350, 300, 250, 250, 400], [300, 450, 100, 200, 200, 300, 350, 50, 450, 250]]
# c fopnr глючный сет