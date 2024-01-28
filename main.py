import discord
import dhooks
import requests
import time
import tweepy
import twilio
from twilio.rest import Client

from commands import commands

# discord api
DISCORD_TOKEN = "TOKEN_HERE"

# twitter api
api_key = 'API_KEY'
api_key_secret = 'API_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# initialize tweepy
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
tweepyApi = tweepy.API(auth)

# twilio api
account_sid = ''
auth_token = ''
twilioClient = Client(account_sid, auth_token)

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):

	# twitter success
	if message.channel.name == "success":
		await commands.post_twitter(tweepyApi, message)
		return

	# keyword pinger
	await commands.keywordPinger(client, message)

	# size converter
	if message.content.startswith("w!sizing"):
		
		await commands.sizing(message)


	# currency converter
	if message.content.startswith("w!forex"):
		
		await commands.currency(message)

	# ebay views
	if message.content.startswith("w!ebay"):
		
		await commands.ebay(message)	

	# ebay watch

	# addy jigger
	if message.content.startswith("w!address"):
		
		await commands.address(message)

	# channel archive
	if message.content.startswith("w!archive"):
		
		await commands.archive(message)

	# delay calc
	if message.content.startswith("w!delay"):
		
		await commands.delay(message)

	# fee calc
	if message.content.startswith("w!fee"):

		await commands.fee(message)

	# gmail dot trick
	if message.content.startswith("w!gmail"):
		
		await commands.email(message)

	# sms
	if message.content.startswith("w!sms"):
		
		await commands.sms(twilioClient, client, message)

	if message.content.startswith("w!addnumber"):

		await commands.add_number(client, message)

	# snowflake
	if message.content.startswith("w!snowflake"):
		
		await commands.snowflake(message)





client.run(DISCORD_TOKEN)


