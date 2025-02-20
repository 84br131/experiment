import discord
from discord.ext import commands
import random
import os
import requests

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

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

@bot.command()
async def memes(ctx):
    imagenes = os.listdir('imagenes')
    with open(f'imagenes/{random.choice(imagenes)}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)

def get_fox_image_url():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['image']

@bot.command()
async def fox(ctx):
    image_url = get_fox_image_url()
    await ctx.send(image_url)

@bot.command()
async def poke(ctx,arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/"+pokemon)
        if result.text == "Not Found":
            await ctx.send("Pokemon no encontrado")
        else:
            image_url = result.json()["sprites"]["front_default"]
            print(image_url)
            await ctx.send(image_url)
    except Exception as e:
        print("Error:", e)

def get_cat_image_url():
    url = 'https://api.thecatapi.com/v1/images/search'
    res = requests.get(url)
    data = res.json()
    return data[0]['url']

@bot.command()
async def gato(ctx):
    image_url = get_cat_image_url()
    await ctx.send(image_url)

def get_advice():
    url = 'https://api.adviceslip.com/advice'
    res = requests.get(url)
    data = res.json()
    return data['slip']['advice']

@bot.command()
async def consejo(ctx):
    advice = get_advice()
    await ctx.send(f"💡 Consejo: {advice}")

@poke.error
async def error_type(ctx,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("Tienes que darme un pokemon")

@bot.command()
async def contaminacion(ctx):
    await ctx.send(f"""
    Hola, soy un bot {bot.user}!
    """)

    await ctx.send("¿Quieres conocer de qué trata la contaminación? Responde 'si' o 'no'.")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in ['si', 'no']
    response = await bot.wait_for('message', check=check)
    
    if response:
        if response.content == "si":
            await ctx.send(""" 
            La contaminación afecta a los grandes ecosistemas naturales que tenemos, como las selvas y los bosques...
            También hace que la temperatura en el planeta aumente, generando el calentamiento global.
            """)

        else:
            await ctx.send("Está bien, si alguna vez necesitas saber sobre otro tema, estaremos en contacto.")
            return

    await ctx.send("¿Quieres más ejemplos sobre contaminación? Responde 'si' o 'no'.")
    def check1(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in ['si', 'no']
    response1 = await bot.wait_for('message', check=check1)
    
    if response1:
        if response1.content == "si":
            await ctx.send("""
            El calentamiento global hace que los polos se descongelen, por lo tanto el nivel de los mares aumenta.
            Provocando así la muerte de la fauna y la flora que habita en esas zonas.
            """)
        else:
            await ctx.send("Está bien, si alguna vez necesitas hablar sobre otro tema, estaremos en contacto.")
            return

    await ctx.send("¿Te gustaría conocer algunas soluciones para reducir la contaminación? Responde 'si' o 'no'.")
    def check2(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in ['si', 'no']
    response2 = await bot.wait_for('message', check=check2)

    if response2:
        if response2.content == "si":
            await ctx.send("""
            Aquí tienes algunas acciones para reducir la contaminación:
            - Usar energías renovables como solar y eólica.
            - Fomentar el transporte público y la movilidad eléctrica.
            - Crear más ciclovías y zonas peatonales.
            - Promover el carpooling y el teletrabajo.
            - Implementar programas de reciclaje y reutilización.
            - Reducir plásticos de un solo uso.
            - Fomentar el compostaje de desechos orgánicos.
            - Incluir educación ambiental en escuelas y universidades.
            - Crear campañas de concienciación sobre contaminación.
            - Aplicar regulaciones estrictas a industrias contaminantes.
            - Multar a empresas que contaminen y premiar a las sostenibles.
            - Impulsar la reforestación masiva.
            - Proteger bosques y ecosistemas naturales.
            """)

    await ctx.send("¿Te gustaría que te envíe una foto sobre un ejemplo de contaminación? Responde 'si' o 'no'.")
    def check3(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in ['si', 'no']
    response3 = await bot.wait_for('message', check=check3)
    
    if response3:
        if response3.content == "si":
            image_path = 'imagenes/contaminacion.jpg'

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    picture = discord.File(f)
                    await ctx.send("Aquí tienes un ejemplo de contaminación:", file=picture)
            else:
                await ctx.send("Lo siento, no pude encontrar la imagen. Verifica que la ruta sea correcta.")
        else:
            await ctx.send("Está bien, si alguna vez necesitas información sobre otro tema, estaré aquí.")



bot.run("Token aquí")
