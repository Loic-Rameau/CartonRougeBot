import os
import discord
from dotenv import load_dotenv
import cartons

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_reaction_add(reaction, user):
    if [cartons.ROUGE, cartons.JAUNE].index(reaction.emoji.id) >= 0:
        print(f'{reaction.emoji} ramasé par {user.name}')
        await cartons.addCarton(reaction.message.author, reaction.emoji.id, reaction.message.channel)


client.run(TOKEN)
