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
		embed.add_field(name="%d -- %s" % (floor.number, floor.name), value=floor.description, inline=False)
	await client.say(embed=embed)

def get_floor(level):
	for floor in FLOORS:
		if floor.number == level:
			return floor
	return None

client.run(TOKEN)
