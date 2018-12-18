import discord
from discord.ext import commands

with open("token.txt") as token_file
    TOKEN = token_file.read().strip()

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Initialized")

client.run(TOKEN)
