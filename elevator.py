import discord
from discord.ext import commands
from time import sleep

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
floor_roles = [r.name for r in FLOORS]

@client.event
async def on_ready():
	print("Initialized")

@client.event
async def on_member_join(member):
	role = discord.utils.get(member.server.roles, name="Ground Level")
	await client.add_roles(member, role)

@client.command(pass_context=True)
async def floor(ctx, level):
	member = ctx.message.author
	channel = ctx.message.channel
	if channel.name == "elevator":
		print("floor command: command used in #elevator")
		try:
			floor = get_floor(int(level))
			if floor:
				print("         ... : got floor from level parameter")
				current_role = None
				for r in member.roles:
					if r.name in floor_roles:
						current_role = r
				if r:
					print("         ... : found current floor of user")
					new_role = discord.utils.get(member.server.roles, name=floor.name)
					print("         ... : got new floor role")
					if new_role.name == current_role.name:
						print("         ... : already on target floor")
						await client.say("Oh? You're already on that floor.")
					else:
						print("         ... : target floor is new floor")
						await client.remove_roles(member, current_role)
						print("         ... : removed current floor role")
						if floor_roles.index(new_role.name) > floor_roles.index(current_role.name):
							await client.say("Going up!")
						else:
							await client.say("Going down!")
						print("         ... : about to sleep...")
						sleep(4)
						print("         ... : sleep done")
						await client.add_roles(member, new_role)
						print("         ... : added new role to user")
						await client.say("Ding!")
						print("         ... : done")
				else:
					print("         ... : user has no floor role")
					await client.say("Uh oh, it seems like you're not currently on any floors. You should contact someone in the maintenence crew.")
			else:
				print("         ... : level given not a valid floor")
				await client.say("Sorry, that's not a valid floor number. Use `.floors` to get a list of available floors.")
		except:
			print("         ... : exception occured in floor command")
			await client.say("Error in floor command!")
	else:
		print("floor command: command used outside of #elevator")

@client.command(pass_context=True)
async def floors(ctx):
	channel = ctx.message.channel
	if channel.name == "elevator":
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
	await client.say("Aauughhh! :dizzy_face:")
	await client.logout()

@client.event
async def on_message(message):
	channel = message.channel
	author = message.author
	content = message.content
	if author != client.user:
		try:
			logs = discord.utils.get(author.server.channels, name="chat-logs")
			await client.send_message(logs, "`#{}` **{}**: {}".format(channel, author, content))
			await client.process_commands(message)
		except:
			print("Message unable to be logged")

@client.event
async def on_message_edit(original, new):
	author = new.author
	channel = new.channel
	old_content = original.content
	new_content = new.content
	if author != client.user:
		try:
			logs = discord.utils.get(author.server.channels, name="chat-logs")
			embed = discord.Embed(title="Message Edited", color=0xFFFF00)
			embed.add_field(name="User", value=author, inline=False)
			embed.add_field(name="Old Message", value=old_content, inline=True)
			embed.add_field(name="New Message", value=new_content, inline=True)
			embed.set_footer(text="Channel: #{}".format(channel))
			await client.send_message(logs, embed=embed)
		except:
			print("Edit unable to be logged")

@client.event
async def on_message_delete(message):
	channel = message.channel
	author = message.author
	content = message.content
	if author != client.user:
		try:
			logs = discord.utils.get(author.server.channels, name="chat-logs")
			embed = discord.Embed(title="Message Deleted", color=0xFF0000)
			embed.add_field(name="User", value=author, inline=False)
			embed.add_field(name="Deleted Message", value=content, inline=True)
			embed.set_footer(text="Channel: #{}".format(channel))
			await client.send_message(logs, embed=embed)
		except:
			print("Deletion unable to be logged")

@client.command(pass_context=True)
async def clear(ctx, amount=100):
	channel = ctx.message.channel
	author = ctx.message.author
	if amount != 100:
		messages = int(amount)
	else:
		messages = 100
	await client.purge_from(channel, limit=1)
	num = len(await client.purge_from(channel, limit=messages))
	try:
		logs = discord.utils.get(author.server.channels, name="chat-logs")
		await client.send_message(logs, "**{}** *purged {} message(s) in* `#{}`".format(author, num, channel))
	except:
		print("Purge unable to be logged")

client.run(TOKEN)
