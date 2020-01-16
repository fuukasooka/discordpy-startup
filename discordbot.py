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
        m = re.match(r"^(\d+)[dD](\d+)$", msg.content)
        if not m:
            return

        # 入力された内容を受け取る
        order = int(m.group(1))  #dice を振る回数
        mx = int(m.group(2))     #dice の出目

        if (order > 100) or (0 >= order):
            await msg.channel.send(msg.author.mention + " Sorry.. Order value:M is invalid. (Valid values are 1-100.)")
            return 

        if (mx > 1000) or (0 >= mx):
            await msg.channel.send(msg.author.mention + " Sorry.. Dice value:N is invalid. (valid value are 1-1000)")
            return

        result = diceroll(order, mx)        # mx面ダイスをorder回振る関数
        await msg.channel.send(msg.author.mention + " to order: " + str(order)+"d"+str(mx))
        await msg.channel.send("total: " + str(sum(result)) +" [" + ",".join(map(str,result)) + "]")

    except Exception as e:                  #エラーハンドリング
        await msg.channel.send(e)
        print(e)

client.run(token)