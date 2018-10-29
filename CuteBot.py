import discord
from discord.ext import commands
from discord.utils import get
import asyncio

f = open("classList.txt")
classList = [[]]
try:
	for x in f:
		x = x.rstrip('\n').upper().split(" ")
		classList.append(x)
finally:
	if f is not None:
		f.close()
	classList.__delitem__(0)

e = open("enrolledList.txt")
enrolledList = [[]]
try:
	for x in e:
		x = x.rstrip('\n').upper().split(" ")
		enrolledList.append(x)
finally:
	if f is not None:
		f.close()
	enrolledList.__delitem__(0)

TOKEN = ''

client = commands.Bot(command_prefix="!")
server = discord.Server(id='482530936412700703')

# Code to cycle server icon
# async def my_background_task():
# 	await client.wait_until_ready()
# 	i = 0
# 	iconDir = ''
# 	CNTSserver = client.get_server('490213374974754837')
# 	while not client.is_closed:
# 		if i == 0:
# 			iconDir = 'SLC_Icon_1.png'
# 			i += 1
# 		elif i == 1:
# 			iconDir = 'SLC_Icon_2.png'
# 			i += 1
# 		else:
# 			iconDir = 'SLC_Icon_3.png'
# 			i = 0
# 		with open(iconDir, 'rb') as f:
# 			icon = f.read()
# 		await client.edit_server(CNTSserver, icon=icon)
# 		await asyncio.sleep(10000) # task runs every 10000seconds


@client.event
async def on_ready():
	print("Bot is online and connected to Discord")


@client.event
async def on_message(message):
	await client.process_commands(message)


# Print a Cookie
@client.command()
async def cookie():
	await client.say(':cookie:')


# Show CommandList
@client.command()
async def commands():
	with open("commandList.txt") as c:
		await client.say(c.read())


# Ping Pong!
@client.command(pass_context=True)
async def ping(ctx):
	userID = ctx.message.author.id
	await client.say('<@{}> Pong!'.format(userID))


# The main enroll command.
@client.command(pass_context=True)
async def enroll(ctx, *args):
	if args and (ctx.message.channel.id == '500067398259441664'):
		args = sorted(args)
		content = " ".join(args[0:]).upper()
		name = ""
		userID = ctx.message.author.id
		member = ctx.message.author
		enrolled = 0
		errorMsg = "<@{}> Something went wrong. Please make sure you type your name as it is on the attendance sheet".format(
			userID)
		for i in enrolledList:
			if i[(len(i)-1)] == userID:
				await client.say("<@{}> you are already enrolled.".format(userID))
				enrolled = -1
		try:
			eL = open("enrolledList.txt", "a")
			cL = open("classList.txt", "w")
			sL = open("serverLog.txt", "a")
		except IOError as io:
			print(io)
			await client.say("IOError, please try again in a few seconds.")
		else:
			if enrolled != -1:
				for idx, val in enumerate(classList):
					tmpName = (" ".join(val[0:(len(val)-1)]))
					if content == tmpName:
						name = tmpName
						year = val[(len(val)-1)]
						enrolled = 1
						if val[(len(val) - 1)] == "2":
							# Add Second Year role
							secondYearRole = get(ctx.message.server.roles, name='Second Year')
							enrolledRole = get(ctx.message.server.roles, name='Enrolled')
							await  client.add_roles(member, enrolledRole, secondYearRole)
						else:
							# Add Enrolled role
							enrolledRole = get(ctx.message.server.roles, name='Enrolled')
							await  client.add_roles(member, enrolledRole)
						classList.__delitem__(idx)
				if enrolled == 1:
					await client.say("<@{}> you are enrolled!".format(userID))
					sL.write(name + " has enrolled.\n")
					# Write to EnrolledList.txt
					entry = [name, year, userID]
					enrolledList.append(entry)
					eL.write(" ".join(entry[0:])+"\n")
			if enrolled == 0:
				await client.say(errorMsg)
			for q in classList:
				cL.write(" ".join(q[0:])+"\n")
		finally:
			if cL is not None:
				cL.close()
			if eL is not None:
				eL.close()
			if sL is not None:
				sL.close()
		await client.delete_message(ctx.message)


# When a member joins check if they are on the enrolled list and if they are give them their roles.
@client.event
async def on_member_join(member):
	channel = member.server.get_channel("500067398259441664")
	userID = member.id
	welcomeMsg = "Welcome <@{}>! You are not Enrolled, please enroll.".format(userID)
	welcomeBack = "Welcome back <@{}>!".format(userID)
	enrolled = 0
	for i in enrolledList:
		if i[(len(i) - 1)] == member.id:
			enrolled = 1
			if x[(len(x) - 2)] == "2":
				secondYearRole = get(member.server.roles, name='Second Year')
				enrolledRole = get(member.server.roles, name='Enrolled')
				await  client.add_roles(member, enrolledRole, secondYearRole)
			else:
				# Add Enrolled role
				enrolledRole = get(member.server.roles, name='Enrolled')
				await  client.add_roles(member, enrolledRole)
	if enrolled == 0:
		await client.send_message(channel, welcomeMsg)
	else:
		await client.send_message(channel, welcomeBack)


# When a member changes their nickname or name log it in serverLog and enrolledList
@client.event
async def on_member_update(before, after):
	if before.nick != after.nick:
		userID = before.id
		enrolled = 0
		tmpName = "NULL"
		for i in enrolledList:
			if i[(len(i)-1)] == before.id:
				enrolled = 1
				tmpName = " ".join(i[0:(len(i) - 2)])
		sL = open("serverLog.txt", "a+")
		try:
			if enrolled == 1:
				if str(after.nick) == "None":
					sL.write(tmpName + " changed their nickname to: " + after.name + ". UserID = " + userID + "\n")
				else:
					sL.write(tmpName + " changed their nickname to: " + str(after.nick) + ". UserID = " + userID + "\n")
			else:
				sL.write(after.name + " changed their nickname to: " + str(after.nick) + ". UserID = " + userID + "\n")
		finally:
			sL.close()
	if before.name != after.name:
		userID = before.id
		enrolled = 0
		tmpName = "NULL"
		for i in enrolledList:
			if i[(len(i) - 1)] == before.id:
				enrolled = 1
				tmpName = before.name
		sL = open("serverLog.txt", "a+")
		try:
			if enrolled == 1:
				sL.write(tmpName + " changed their name to: " + str(after.name) + ". UserID = " + userID + "\n")
			else:
				sL.write(after.name + " changed their name to: " + str(after.name) + ". UserID =  " + userID + "\n")
		finally:
			sL.close()


client.run(TOKEN)
