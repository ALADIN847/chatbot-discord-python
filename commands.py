import discord
import dhooks
import random
import requests
import json
import tweepy
import time
import os
import twilio
from twilio.rest import Client

class commands:

	embed_footer = "AIO DreamBot"
	embed_color = 0x4DF2EC
	image = "https://media.discordapp.net/attachments/756282581359657070/756369590925131886/image0.png"

	twilio_number = "" # +11231231234 | area code + number

	archive_category_id = 783181444872667146

	async def keywordPinger(client, message):
		
		with open("keywordPingerChannels.txt") as keywordCategoryFile:
			allowedChannels = keywordCategoryFile.read().split("\n")
		keywordCategoryFile.close()

		for x in range(len(allowedChannels)):
			try:
				allowedChannels[x] = int(allowedChannels[x])
			except:
				continue

		if message.author.id == client.user.id:
			return
		if message.channel.id not in allowedChannels:
			return

		with open("keywordData.json", "r") as keywordDataFile:
			keywordData = json.loads(keywordDataFile.read())
		keywordDataFile.close()

		for key, value in keywordData.items():

			keyword = key.replace("+", "")
			keyword = keyword.replace(" ", "")
			keyword = keyword.lower()

			keywords = keyword.split(",")

			if message.channel.id in keywordData[key][1]:
				pass
			else:
				return
			
			if all(x in message.content for x in keywords):
				await message.channel.send(keywordData[key][0] + ", keyword: ``{}``".format(key))

			for embed in message.embeds:

				jsonDict = str(embed.to_dict())
				if keyword in jsonDict:
					await message.channel.send(keywordData[key] + ", keyword: ``{}``".format(key))

	async def post_twitter(tweepyApi, message):

		image_url = message.attachments[0].url
		tweet_message = message.content
		if len(tweet_message) > 140:
			tweet_message = "Success from Dreamcook"

		# download temp image
		myfile = requests.get(url)
		open('temp.png', 'wb').write(myfile.content)
		# ---------------------

		try:
			tweet = "{}".format(tweet_message)
			# post to twitter and delete temp image
			tweepyApi.update_with_media('temp.png', tweet)
		except:
			tweet = image_url
			tweepyApi.update_status(tweet)

		os.remove("temp.png")

		await message.channel.send("Your success has been posted.")
		# -----------------------

	async def currency(message):
		
		messageContent = message.content.split(' ')

		if len(messageContent) != 2:
			await commands.error_message(message, "Command Error", "Please use the format, w!forex [Conversion Code, ex. USDGBP]")
			return

		conversionCode = messageContent[1]

		request = requests.get("https://www.freeforexapi.com/api/live?pairs={}".format(conversionCode))

		response = json.loads(request.text)

		if response["code"] == 1002:

			supportedPairs = ""
			for x in range(len(response["supportedPairs"])):

				supportedPairs += response["supportedPairs"][x] + ","

			await message.channel.send(response["message"])
			await message.channel.send("Supported Pairs: \n" + supportedPairs)
			return
		if response["code"] == 200:
			
			rate = response["rates"][conversionCode]["rate"]

			n = 3
			codes = [conversionCode[i:i+n] for i in range(0, len(conversionCode), n)]

			await message.channel.send("1 " + codes[0] + " converts to " + str(rate) + " " + codes[1])

	async def ebay(message):

		if len(message.content.split(" ")) != 2:
			await commands.error_message(message, "Command Error", "Please use the format, w!ebay [Ebay Link]")
			return

		ebayLink = message.content.split(" ")[-1]

		await message.author.send("Your request for {} is being processed".format(ebayLink))

	async def address(message):

		address = message.content.split("w!address ")[1]
		addresses = ""

		TRANSLATIONS = [
			["street", "st.", "st"],
			["drive", "dr.", "dr"],
			["lane", "ln.", "ln"],
			["avenue", "ave.", "ave"],
			["west", "w.", "w"],
			["east", "e.", "e"],
			["north", "n.", "n"],
			["south", "s.", "s"],
			["east", "e.", "e"],
			["boulevard", "blvd", "blvd."],
			["mountain", "mtn.", "mtn"],
			["court", "ct.", "ct"]
		]

		UNITS = [
			"Unit 1", "Unit 2", "Unit 3", "Room A", "Room B", "Room C"
		]

		coin = [True, False]

		try:
			for w in range(10):
				for x in range(len(TRANSLATIONS)):
					
					for y in range(len(TRANSLATIONS[x])):

						if TRANSLATIONS[x][y] in address.split(" "):

							randomSuffix = random.choice(TRANSLATIONS[x])

							new_address = address.replace(TRANSLATIONS[x][y], randomSuffix)

							if random.choice(coin):
								new_address = new_address + " " + random.choice(UNITS)

			
							addresses += new_address + "\n"
						else:
							pass

			await message.channel.send(addresses)
		except:
			await message.channel.send("Address currently not supported, please dm <@263445930429120512> an example of your address and possible alternative options.", delete_after = 5)
			await message.delete()

	async def archive(message):
		
		messageContent = message.content.split(' ')

		if len(messageContent) != 2:
			await commands.error_message(message, "Command Error", "Please use the format, w!archive [Channel ID]")
			return

		channel_id = int(messageContent[1])

		categories = message.guild.categories
		category = None
		for x in range(len(categories)):
			if categories[x].id == commands.archive_category_id:
				category = categories[x]
				break
		if category == None:
			return

		channel = message.guild.get_channel(channel_id)

		if channel == None:
			
			await message.channel.send("Channel could not be found")

		await channel.edit(category = category)

	async def delay(message):
		
		messageContent = message.content.split(' ')

		if len(messageContent) != 3:
			await commands.error_message(message, "Command Error", "Please use the format, w!delay [Number of Proxies] [Number of Tasks]")
			return

		proxies = int(messageContent[1])
		tasks = int(messageContent[2])

		delay = (3500 * tasks) / proxies

		await message.channel.send('For ' + messageContent[1] + ' proxies and ' + messageContent[2] + ' tasks, use a ' + str(delay) + ' ms delay.')

	async def fee(message):

		messageContent = message.content.split(' ')

		if len(messageContent) != 2:
			await commands.error_message(message, "Command Error", "Please use the format, w!fee [listing price]")
			return


		stockx1 = (1 - .125) * float(messageContent[1])
		stockx2 = (1 - .12) * float(messageContent[1])
		stockx3 = (1 - .115) * float(messageContent[1])
		stockx4 = (1 - .11) * float(messageContent[1])
		goat1 = (1 - .18) * float(messageContent[1])
		goat2 = (1 - .125) * float(messageContent[1])
		ebay = 1 * float(messageContent[1])

		embedFee = dhooks.Embed(
			title = 'Fee Calculator',
			description = 'Find out payout from popular seller platforms!',
			color = commands.embed_color
			)
		embedFee.set_footer(commands.embed_footer, commands.image)

		embedFee.add_field(name = 'Inputted price: ', value = str(messageContent[1]), inline = False)
		embedFee.add_field(name = 'StockX Level 1: ', value = str('{:.2f}'.format(stockx1)), inline = False)
		embedFee.add_field(name = 'StockX Level 2: ', value = str('{:.2f}'.format(stockx2)), inline = False)
		embedFee.add_field(name = 'StockX Level 3: ', value = str('{:.2f}'.format(stockx3)), inline = False)
		embedFee.add_field(name = 'StockX Level 4: ', value = str('{:.2f}'.format(stockx4)), inline = False)
		embedFee.add_field(name = 'Goat Rating 89-70: ', value = str('{:.2f}'.format(goat1)), inline = False)
		embedFee.add_field(name = 'Goat Rating 90+: ', value = str('{:.2f}'.format(goat2)), inline = False)
		embedFee.add_field(name = 'Ebay (Athletic Shoes only): ', value = str('{:.2f}'.format(ebay)), inline = False)

		await message.channel.send(embed = embedFee)

	async def email(message):
		
		messageContent = message.content.split(' ')

		if len(messageContent) != 3:
			await commands.error_message(message, "Command Error", "Please use the format, w!gmail [Your Gmail] [Amount]")


		email = messageContent[1]

		email_parts = email.split('@')

		if email_parts[1] != "gmail.com":
			
			await message.channel.send("Please use a gmail account")
			return

		address_field = list(email_parts[0])

		new_address_list = ""
		new_address = ""

		for y in range(int(messageContent[2])):

			new_address = ""
			for x in range(len(address_field)):
				
				new_address += address_field[x]

				choice = [True, False]

				if random.choice(choice) == True:
					
					new_address += "."

			new_address_list += new_address + "@gmail.com\n"

		await message.channel.send(new_address_list) 

	async def sizing(message):
		
		image_link = "https://i.pinimg.com/originals/b5/bc/80/b5bc808f6a5fb2a1182c772410867f91.jpg"

		await message.channel.send(image_link)

	async def sms(twilioClient, client, message):

		with open("phoneNumbers.json", "r") as phoneNumberFile:
			numbersJSON = json.load(phoneNumberFile)
		phoneNumberFile.close()

		numbers = list(numbersJSON.values())

		introEmbed = dhooks.Embed(
			title = "SMS",
			color = commands.embed_color,
			description = "Welcome to DreamCook SMS. Please enter the message you would like to send."
			)

		await message.channel.send(embed = introEmbed)

		textMessageText = await client.wait_for('message')
		while textMessageText.channel != message.channel:
			textMessageText = await client.wait_for('message')


		await message.channel.send("Please confirm with 'y' or 'n' if you are ready to send the following message to {} users.".format(len(numbers)))
		await message.channel.send(textMessageText.content)

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




		invalidNumbers = []

		for x in range(len(numbers)):
			number = numbers[x]

			# will send 10 messages in 3 seconds
			try:
				message = twilioClient.messages.create(
			                              body = textMessageText.content,
			                              from_ = commands.twilio_number,
			                              to = number
			                          )
			except twilio.base.exceptions.TwilioRestException as error:
				print("{} was an invalid phone number".format(phone))
				invalidNumbers.append(phone)
				continue

			print("Sent Message to number {}".format(number))

		return

	async def add_number(client, message):

		with open("phoneNumbers.json", "r") as phoneNumberFile:
			numbersJSON = json.load(phoneNumberFile)
		phoneNumberFile.close()

		discord_id = message.author.id

		introEmbed = dhooks.Embed(
			title = "SMS Update",
			color = commands.embed_color,
			description = "Welcome to DreamCook SMS. Please enter the number you would like to send to. Please include your area code as well. Ex. '+14691231234'"
			)

		await message.channel.send(embed = introEmbed)
	
		number = await client.wait_for('message')
		while number.channel != message.channel:
			number = await client.wait_for('message')

		numbersJSON[str(discord_id)] = number.content


		with open('phoneNumbers.json','w') as phoneNumberFile:
			json.dump(numbersJSON, phoneNumberFile, indent = 4)
		phoneNumberFile.close()

		await message.channel.send("Your phone number has been updated to {}".format(number.content))

	async def snowflake(message):
		
		messageContent = message.content.split(' ')

		if len(messageContent) != 2:
			await commands.error_message(message, "Command Error", "Please use the format, w!snowflake [id]")
			return

		obj = discord.Object(messageContent[1])

		time = obj.created_at

		await message.channel.send(str(time))

	async def error_message(message, title, description):

		channel = message.channel

		errorEmbed = dhooks.Embed(
			title = title,
			color = commands.embed_color,
			description = description
			)
		errorEmbed.set_footer(commands.embed_footer, commands.image)

		await channel.send(embed = errorEmbed)


