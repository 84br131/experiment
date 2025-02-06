import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def suma(ctx, n1: int, n2: int):
    await ctx.send(f"La suma de {n1} y {n2} es {n1 + n2}")

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.lower().split('d'))
    except Exception:
        await ctx.send('El formato debe ser NdN (ejemplo: 2d6).')
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)

@bot.command()
async def choose(ctx, *choices: str):
    if choices:
        await ctx.send(random.choice(choices))
    else:
        await ctx.send("Debes proporcionar opciones para elegir.")

@bot.command()
async def repeat(ctx, times: int, *, content="repitiendo..."):
    for _ in range(min(times, 5)):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send(f'{member.name} se unió el {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def limpiar(ctx):
    await ctx.channel.purge()
    await ctx.send("Mensajes eliminados", delete_after = 3)

bot.run("MTMzNDMwMTc2Mzg4ODc0MjQyMQ.GA3hXP.gL-KeWReUkp0eLo4R2gvM2xElQr7QqNklDHsKY")
