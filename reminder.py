import discord
import dhooks
import requests
import time
import tweepy
import datetime

DISCORD_TOKEN = "TOKEN_HERE"


client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):

	if message.content.startswith("r!new"):

		introEmbed = dhooks.Embed(
			title = "Reminder",
			color = 0x121212,
			description = "Welcome to DreamCook Reminders. Please enter the id of the message you would like to recreate."
			)

		await message.channel.send(embed = introEmbed)

		messageID = await client.wait_for('message')
		while messageID.channel != message.channel:
			messageID = await client.wait_for('message')

		remindedMessage = await message.channel.fetch_message(int(messageID.content))

		channelEmbed = dhooks.Embed(
			title = "Channel",
			color = 0x121212,
			description = "Please enter the id of the channel you want to send this message to."
			)

		await message.channel.send(embed = channelEmbed)

		channelID = await client.wait_for('message')
		while channelID.channel != message.channel:
			channelID = await client.wait_for('message')

		remindedChannel = client.get_channel(int(channelID.content))

		timeEmbed = dhooks.Embed(
			title = "Channel",
			color = 0x121212,
			description = "Please enter the time of when you want this message to send. Use the following format in UTC time zone, YY MM DD HH MM SS"
			)

		await message.channel.send(embed = timeEmbed)

		timeInput = await client.wait_for('message')
		while timeInput.channel != message.channel:
			timeInput = await client.wait_for('message')


		timeValues = timeInput.content.split(" ")
		print(timeValues)
		while len(timeValues) != 6:
			await message.channel.send("Incorrect format, please try again.")
			timeEmbed = dhooks.Embed(
				title = "Channel",
				color = 0x121212,
				description = "Please enter the time of when you want this message to send. Use the following format in UTC time zone, DD MM YY HH MM SS"
				)

			await message.channel.send(embed = timeEmbed)

			timeInput = await client.wait_for('message')
			while timeInput.channel != message.channel:
				timeInput = await client.wait_for('message')

		try:
			plannedTime = datetime.datetime(int(timeValues[0]), int(timeValues[1]), int(timeValues[2]), int(timeValues[3]), int(timeValues[4]), int(timeValues[5]))
		except:
			await message.channel.send("Your date/time was invalid, please restart")
			return

		await message.channel.send("Please confirm with 'y' or 'n' if you are ready to send this message at {} UTC.".format(plannedTime))
		await message.channel.send(remindedMessage.jump_url)


		confirm = await client.wait_for('message')
		while confirm.channel != message.channel:
			confirm = await client.wait_for('message')


		if confirm.content == "y":
			pass
		elif confirm.content == "n":
			await message.channel.send("Until next time...")
			return
		elif confirm.content != "y" and confirm.content != "n":
			await message.channel.send("Incorrect input, please try again.")
			if confirm.content == "y":
				pass
			if confirm.content == "n":
				await message.channel.send("Until next time...")
				return


		await message.channel.send("Reminder set, please standy.")


		now = datetime.datetime.now()

		remainingTime = plannedTime - now

		print(remainingTime.total_seconds())

		while remainingTime.total_seconds() > 0:
			
			time.sleep(5)

			now = datetime.datetime.now()

			remainingTime = plannedTime - now

			print(remainingTime.total_seconds())

		await remindedChannel.send(content = remindedMessage.content)










client.run(DISCORD_TOKEN)