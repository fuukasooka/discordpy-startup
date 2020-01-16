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
    channel = client.get_channel('チャンネルID')
    await channel.send('ダイスロールは任せろ―！ばりばり～')

@client.event
async def on_message(msg):
    #bot空の発言は無視
    if msg.author.bot:
        return
    #オーダーを含む発言にマッチするか
    m = re.match(r"^!d(?:ice)?\s(\d+)d(\d+)$", msg.content.lower())
    if m:
        await  msg.channel.send("OK:"+msg.author)
    else:
        await  msg.channel.send("Invalid value. Write like MdN. (M and N are integers)")
        return

    # 入力された内容を受け取る
    order = m.group(1)  #dice を振る回数
    mx = m.group(2)   #dice の出目

    if order >= 100 :
        msg.channel.send("Sorry.. Order value:M is invalid. (Valid values are 1-100.)")
        return 

    resalt = diceroll(order, mx) # m面ダイスをn回振る関数
    await msg.channel.send(sum(resalt)) # さいころの総和を表示
    await msg.channel.send(dice)        # さいころの目の内訳を表示する

client.run(token)