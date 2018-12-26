import discord
from discord.ext import commands
from time import sleep

players = {}
runtime = {}

class Floor:
	def __init__(self, number, name, description):
		self.number = number
		self.name = name
		self.description = description

with open("token.txt") as token_file:
	TOKEN = token_file.read().strip()

client = commands.Bot(command_prefix='.')

FLOORS = [
	Floor(-2, "Garage Level 2", "Parking Garage B"),
	Floor(-1, "Garage Level 1", "Parking Garage A"),
	Floor(0, "Ground Level", "The Lobby"),
	Floor(1, "Floor 1", "Science"),
	Floor(2, "Floor 2", "Art"),
	Floor(3, "Floor 3", "Tech"),
	Floor(4, "Floor 4", "Animals"),
	Floor(5, "Floor 5", "Literally Just Screaming"),
	Floor(6, "Floor 6", "Courage the Cowardly Dog Roleplay"),
	Floor(7, "Floor 7", "Hotdog vs. Cheeseburger Supremacy"),
	Floor(8, "Floor 8", "Whale Facts"),
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
	server = member.server
	vc = member.voice.voice_channel
	if vc == discord.utils.get(server.channels, name="General", type=discord.ChannelType.voice) \
		and not client.is_voice_connected(server):
		try:
			await client.join_voice_channel(vc)
			voice_client = client.voice_client_in(server)
			player = voice_client.create_ffmpeg_player("Elevator Music.mp3")
			players[server.id] = player
			player.start()
			player.pause()
			runtime[server.id] = 0
		except:
			print("Unable to join voice channel.")
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
				if current_role:
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
						try:
							players[server.id].resume()
							runtime[server.id] += 5
						except:
							print("No player found")
						sleep(5)
						try:
							if runtime[server.id] >= 60:
								players[server.id].stop()
								await client.voice_client_in(server).disconnect()
						except:
							print("No player found")
						try:
							players[server.id].pause()
						except:
							print("No player found")
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

@client.command()
async def kill():
	print("Kill command received. Exiting...")
	await client.say("Aauughhh! :dizzy_face:")
	await client.logout()

client.run(TOKEN)
