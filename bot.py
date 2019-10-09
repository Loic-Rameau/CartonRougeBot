import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import cartons

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


@bot.command(name="combien", help="Donne les totaux des cartons")
async def combien(ctx):
    message = []
    for carton in cartons.fethAllCartons():
        user = discord.utils.find(lambda u: u.id == carton.user, bot.users)
        emoji = discord.utils.find(lambda e: e.id == carton.carton, bot.emojis)
        message.append(f'{user.name} à {carton.nb} <:{emoji.name}:{carton.carton}>')
    if len(message) == 0:
        message.append('Aucun carton')
    await ctx.send("\n".join(message))


@bot.command(name="carton", help="Donne les totaux de tes cartons")
async def carton(ctx, pseudo=''):
    if pseudo == '':
        pseudo = ctx.author.name
    u = discord.utils.find(lambda u: u.name == pseudo, bot.users)
    print(f'showing carton pour {pseudo}({u.id})')
    message = []
    for carton in cartons.fethAllCartons():
        if carton.user != u.id:
            continue
        emoji = discord.utils.find(lambda e: e.id == carton.carton, bot.emojis)
        message.append(f'{u.name} à {carton.nb} <:{emoji.name}:{carton.carton}>')
    if len(message) == 0:
        message.append('Aucun carton')
    await ctx.send("\n".join(message))


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


bot.run(TOKEN)
