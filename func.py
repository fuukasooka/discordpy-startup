import random
import re

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

def calc(cmd: str):
    res = ""
    c = re.match(r"^(\d+(?:[d]\d+)?)([+-].*)?$",cmd)
    if not c :
        res += "_不正な式です_"
        return 0, res
    item = c.group(1)            
    s_item = c.group(2)
    if 'd' in item:
        (order,dice) = map(int,item.split('d'))
        d = diceroll(order,dice)
        cul = sum(d)
        detile = ' ,'.join(map(str,d))
        res += item + f"({cul})[{detile}]"
    else :
        cul = int(item)
        res += str(cul)
    if s_item :
        if s_item[0] == "-":
            a , b = calc(s_item[1:])
            return [cul - a, res + s_item[0] + str(b)]
        elif s_item[0] == "+":
            a , b = calc(s_item[1:])
            return [cul + a, res + s_item[0] + str(b)]
    else :
        return cul , res


def calc_1d100(add_dice: int,target_value: int):
    res = ""
    ttl = ""
    item = "1d100"
    opt = ""      
    b = False
    p = False
    t = False
    add = 0
    if 0 < target_value:
        t = True
        ttl += f"(目標:{target_value}) " 

    if add_dice < 0:
        p = True
        add = - add_dice
        ttl += f"(ペナルティダイス:{add}) "
    elif add_dice > 0:
        b = True
        add = add_dice
        ttl += f"(ボーナスダイス:{add}) "

    (order,dice) = map(int,item.split('d'))
    d = diceroll(order,dice)
    cul = sum(d)
    
    for i in range(add):
        v_1 = cul % 10
        v_10 = 10 * sum (diceroll(1,10))
        v = v_1 + v_10
        if v >100:
            v-= 100
        d.append(v)

    if p:
        cul = max(d)
    elif b:
        cul = min(d)

    t_m = ""
    if t :
        fnb = 96
        s_r = int(target_value )
        s_h = int(target_value / 2)
        s_e = int(target_value / 5)
        s_c = 1
        if s_c >= cul:
            t_m = f"\n ⇒ クリティカル!!!"
        elif s_e >= cul:
            t_m = f"\n ⇒ 成功（イクストリーム）"
        elif s_h >= cul:
            t_m = f"\n ⇒ 成功（ハード）"
        elif s_r >= cul:
            t_m = f"\n ⇒ 成功（レギュラー）"
        elif fnb > cul:
            t_m = f"\n ⇒ 失敗"
        elif cul >= fnb:
            t_m = f"\n ⇒ ファンブル"

    detile = ' or '.join(map(str,d))
    res = item + opt + f"({cul})[{detile}]" + t_m
    ttl = str(cul) + ttl

    return ttl , res
