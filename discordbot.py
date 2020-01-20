import discord
import sys
import os
import re

# さいころの和を計算する用の関数
from func import  diceroll

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
        hide = False
        result = "aaa"
        total = 0

        def calc(cmd):
            res = ""
            c = re.match(r"^(\d+(?:[d]\d+)?)([+-].*)?$",cmd)
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
                res += s_item[0] 
                if s_item[0] == "-":
                    a , b = calc(s_item[1:])
                    return [cul - a, res + str(b)]
                elif s_item[0] == "+":
                    a , b = calc(s_item[1:])
                    return [cul + a, res + str(b)]
            else :
                return cul , res

        total ,result = calc(cmd)
        for opt in cmd_l:
            prm = opt[0:2] 
            if prm == "-t":
                t = int(opt[2:])
            elif prm == "-h" or opt == "hide":
                h = True
            elif prm == "-p":
                p = int(opt[2:])
            elif prm == "-b":
                b = int(opt[2:])
            elif opt == "help":
                print("Help")
            else:
                raise ValueError(opt + ":オプションは存在しません")


        # 入力された内容を受け取る
        if hide:
            #DMに送信
            dm = await msg.author.create_dm()
            await dm.send(msg.author.mention + f"結果 : {total} = {result}" )
            await msg.channel.send(msg.author.mention + " : " + f"{msg.content}" + " : ダイレクトメッセージ送ったぞ！")          
        else :
            #メッセージのチャンネルに送信
            await msg.channel.send(msg.author.mention + f"結果 : {total} = {result}" )

    except Exception as e:                  #エラーハンドリング
        await msg.channel.send(e)
        print(e)

client.run(token)