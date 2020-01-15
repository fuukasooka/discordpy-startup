from discord.ext import commands
import os
import traceback
import re

bot = commands.Bot(command_prefix='!')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def dice(ctx, msg):
    m = re.match(r"^\d+d\d+$", msg)
    if m:
        await  ctx.send(msg)    
    else:
        await  ctx.send("Invalid value.Write like NdM. (N and M are integers)")

    cnt, mx = list(map(int, msg.split('d'))) # さいころの個数と面数
    dice = diceroll(cnt, mx) # 和を計算する関数(後述)
        # サイコロの目の総和を表示
    await  ctx.send(sum(dice))
        # さいころの目の内訳を表示する
    await  ctx.send(dice)

bot.run(token)
