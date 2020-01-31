import discord
import sys
import os
import re

# さいころの和を計算する用の関数
from func import  diceroll
from func import  calc
from func import  calc_1d100

#bot = commands.Bot(command_prefix='/')
client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

help_txt = """\
/*********************
 *** Dise-Bot Help ***
 *********************/
テキストチャンネルにダイスロール表記（NdM）の書き込みをすると
自動でダイスを計算してあげるよ。
ついでに定数の足し算引き算くらいなら一緒に計算できるよ。
例）
1d6 →　1d6(5) = 5
2d6+6 →　2d6(7)+6 = 13

注意してほしい点は、同時に触れるダイス数は100までな点と、1000面ダイスまでしか用意していない点だ。
これを超えると僕も計算できないから、その時は自分たちで計算してくれよな。
もっとも、そんな機会はないだろうけどね。
---------------
オプション機能も用意しているよ。計算式の後に空白区切りで追記してくれ。
複数指定することも可能さ。

-h: 隠しダイス機能。ダイスの結果をダイレクトメッセージで君だけに届けるよ。

-p_: ペナルティダイス機能。新COCルルブのペナルティダイス込みでダイスロールしてくれるよ。
    ただし、1d100でしか使えないから注意してね。また、ボーナスダイスオプションと同時使用はできないよ。
    パラメータの後にダイス数を指定できるよ
    例）1d100 -p2 →　1d100<p2> (86)[6 or 46 or 86]

-b_: ボーナスダイス機能。新COCルルブのボーナスダイス込みでダイスロールしてくれるよ。
    ただし、1d100でしか使えないから注意してね。また、ペナルティダイスオプションと同時に使用はできないよ。
    パラメータの後にダイス数を指定できるよ
    例）1d100 -b2 →　1d100<b2> (6)[6 or 46 or 86]

-t_: 目標値判定機能。新COCルルブの目標値の判定をしてくれるよ。
    目標値の半分以下　→　ハード成功！　とかね。
    ただし、まだ実装できていないんだ。ごめんね。
"""

@client.event
async def on_ready():
    print('--------------')
    print('ログインしました')
    print(client.user.name)
    print(client.user.id)
    print('--------------')
#    channel = client.get_channel('チャンネルID')
#    await channel.send('楽しいTRPGを始めましょう！')

@client.event
async def on_message(msg):
    try :
        #botからの発言は無視
        if msg.author.bot:
            return

        #ヘルプ        
        if msg.content.find("dice-bot help") == 0:
            await msg.channel.send(help_txt)
            return

        #オーダーを含む発言にマッチするか
        m = re.match(r"^(\d+)[dD](\d+).*$", msg.content)
        if not m:
            return
        
        #コマンド・オプションを分ける
        cmd_l = msg.content.lower().split(' ')
        cmd = cmd_l.pop(0)

        #初期値の設定
        h = False
        target_value = 0
        result = ""
        total = ""
        add_dice = 0
        #引数
        for opt in cmd_l:
            prm = opt[0:2] 
            if prm == "-t":
                if not opt[2:]:
                    raise ValueError("目標値の設定が必要です")
                    return
                target_value = int(opt[2:])
                if not target_value :
                    raise ValueError("目標値の値が不正です")
                elif target_value <= 0 or 100 < target_value :
                    raise ValueError("目標値の値は1-100までです")
                    return
                if cmd != "1d100":
                    raise ValueError("目標値のダイスオプションは1D100の場合しか指定できません。")
                    return
            elif prm == "-h" or opt == "hide":
                h = True
            elif prm == "-p":
                if not opt[2:]:
                    add_dice = -1
                else :
                    if int(opt[2:]) <= 0:
                        raise ValueError("ペナルティダイスの数が不正です")
                    add_dice = - int(opt[2:])
                if cmd != "1d100":
                    raise ValueError("ペナルティダイスオプションは1D100の場合しか指定できません。")
                    return
            elif prm == "-b":
                if not opt[2:]:
                    add_dice = 1
                else :
                    if int(opt[2:]) <= 0:
                        raise ValueError("ボーナスダイスの数が不正です")
                    add_dice = int(opt[2:])
                if cmd != "1d100":
                    raise ValueError("ボーナスダイスオプションは1D100の場合しか指定できません。")
                    return
            elif opt == "help":
                print("Help")
            else:
                raise ValueError(opt + ":オプションは存在しません")
        if add_dice == 0 and target_value == 0:
            total ,result = calc(cmd)
        else :
            total ,result = calc_1d100(add_dice,target_value)

        # 入力された内容を受け取る
        if h:
            #DMに送信
            dm = await msg.author.create_dm()
            await dm.send(msg.author.mention + f"結果 : {total} = {result}" )
            await msg.channel.send(msg.author.mention + " : " + f"{msg.content}" + " : 結果はダイレクトメッセージに送ったよ")          
        else :
            #メッセージのチャンネルに送信
            await msg.channel.send(msg.author.mention + f"結果 : {total} = {result}" )

    except Exception as e:                  #エラーハンドリング
        await msg.channel.send(e)
        print(e)

client.run(token)