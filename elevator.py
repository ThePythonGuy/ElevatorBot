import discord
from discord.ext import commands

class Floor:
	def __init__(self, number, name, description):
		self.number = number
		self.name = name
		self.description = description

with open("token.txt") as token_file:
	TOKEN = token_file.read().strip()

client = commands.Bot(command_prefix='.')

FLOORS = [
	Floor(0, "Ground Level", "The Lobby"),
	Floor(1, "Floor 1", "Science"),
	Floor(2, "Floor 2", "Art"),
]

@client.event
async def on_ready():
	print("Initialized")

@client.command(pass_context=True)
async def floor(ctx, level):
	member = ctx.message.author
	try:
		floor = get_floor(int(level))
		if floor:
			role_name = floor.name
			role = discord.utils.get(member.server.roles, name=role_name)
			await client.replace_roles(member, role)
			await client.say("Done.")
		else:
			await client.say("Sorry, that's not a valid floor number. Use `.floors` to get a list of available floors.")
	except:
		await client.say("Error while trying to add role!")

@client.command(pass_context=True)
async def floors(ctx):
	embed = discord.Embed(title="Floors", description="The directory of floors in the tower.", color=0xcccccc)
	for floor in FLOORS:
		embed.add_field(name="%d -- %s" % (floor.number, floor.description), value=floor.name, inline=False)
	await client.say(embed=embed)

def get_floor(level):
	for floor in FLOORS:
		if floor.number == level:
			return floor
	return None

@client.command()
async def ping():
	await client.say("Pong!")

@client.command()
async def kill():
	print("Kill command received. Exiting...")
	await client.logout()

@client.event
async def on_message(message):
	author = message.author
	content = message.content
	if author != client.user:
		try:
			channel = discord.utils.get(author.server.channels, name="chat-logs")
			await client.send_message(channel, "**{}**: {}".format(author, content))
			await client.process_commands(message)
		except:
			print("Message unable to be logged")

@client.event
async def on_message_edit(original, new):
	author = new.author
	old_content = original.content
	new_content = new.content
	if author != client.user:
		try:
			channel = discord.utils.get(author.server.channels, name="chat-logs")
			await client.send_message(channel, "**{} edited their message**: \n*old:* {}  \n*new:* {}".format(author, old_content, new_content))
			await client.process_commands(new)
		except:
			print("Edit unable to be logged")

@client.event
async def on_message_delete(message):
	author = message.author
	content = message.content
	if author != client.user:
		try:
			channel = discord.utils.get(author.server.channels, name="chat-logs")
			await client.send_message(channel, "**{} deleted their message**: {}".format(author, content))
			await client.process_commands(message)
		except:
			print("Deletion unable to be logged")

client.run(TOKEN)
