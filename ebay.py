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

	
	if message.content.startswith("w!ebay"):

		await message.author.send("Completing ebay request...")

		message = message.split(' ')
		if len(message) != 2:
			await discord_message.channel.send('Please use the format, !ebay itemLink')
			return
		if not message[1].startswith('https://www.ebay.com/'):
			await discord_message.channel.send('Please use a ebay item link')
			return

		try:
			await discord_message.channel.send('Adding views...')
			for x in range(100):
				requests.get(message[1])
			await message.author.send("Request complete.")
		except requests.exceptions.ProxyError:
			await discord_message.channel.send('Proxy Error, please message dev')









client.run(DISCORD_TOKEN)