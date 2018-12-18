import discord
from discord.ext import commands

with open("token.txt") as token_file:
    TOKEN = token_file.read().strip()

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Initialized")

@client.command()
async def ping():
    await client.say("Pong!")

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    if author != client.user:
        try:
            channel = discord.utils.get(author.server.channels, name="chat-logs")
            await client.send_message(channel, "{}: {}".format(author, content))
            await client.process_commands(message)
        except:
            print("Message unable to be logged")

client.run(TOKEN)
