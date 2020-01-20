import random

def diceroll(cnt: int , max: int):
    total = 0
    num_list = []

    if not(0 < cnt <=100) :
        raise ValueError("Mの有効値は1-100です")
        return 
    if not(0 < max <=1000) :
        raise ValueError("Nの有効値は1-1000です")
        return

    for i in range(0, cnt):
        # ランダムに1からサイコロの面数までの和を取得しリストに入れる
        num = random.randint(1, max)
        num_list.append(num)
    return num_list