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
        
        #オーダーを含む発言にマッチするか
        m = re.match(r"^(\d+)[dD](\d+).*$", msg.content)
        if not m:
            return
        
        #コマンド・オプションを分ける
        cmd_l = msg.content.lower().split(' ')
        cmd = cmd_l.pop(0)

        #初期値の設定
        h = False
        result = ""
        total = 0
        add_dice = 0
        #引数
        for opt in cmd_l:
            prm = opt[0:2] 
            if prm == "-t":
                t = int(opt[2:])
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
        if add_dice == 0 :
            total ,result = calc(cmd)
        else :
            total ,result = calc_1d100(add_dice)
        
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