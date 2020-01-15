from discord.ext import commands
import os
import traceback

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
    await  ctx.send(msg)
    say = msg 
    cnt, mx = list(map(int, order.split('d'))) # さいころの個数と面数
    dice = diceroll(cnt, mx) # 和を計算する関数(後述)
    await  ctx.send(dice[cnt])
        # さいころの目の総和の内訳を表示する
    await  ctx.send(sum(dice))

bot.run(token)
