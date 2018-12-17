import discord
from discord.ext import commands

TOKEN = open("token.txt").readline()

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Initialized")

client.run(TOKEN)
