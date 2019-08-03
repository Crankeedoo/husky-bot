import discord
from discord.ext import commands
import os
import random
import asyncio
import math
import time
import aiohttp
import json
import yarl
from yarl import URL
import html

command_prefix='&'
description = 'A bot for the North Hollywood High School sophomores\' server. If you\'re having an issue with the bot, ask Crankeedoo (Niko) for help.'

bot = commands.Bot(command_prefix=command_prefix, description=description)
client = discord.Client()

@bot.event
async def on_ready():
	# Returns bot's name and id upon startup
	
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def coin():
    # Returns random integer between 1 and 2
    """Flips a coin."""
	
	# Return heads if random integer is 1, tails if random integer is 2
    if random.randint(1,2) == 1:
        await bot.say('Your coin came up heads.')
    else:
        await bot.say('Your coin came up tails.')

@bot.command(pass_context = True)
async def randomuser(ctx):
    # Returns random user from server, mentions them and posts their avatar in an embed
    """Selects a random user from the server."""
	
	# Chooses random user from server where command was used
    server = ctx.message.server
    message = ctx.message
    randomMember = random.choice(list(server.members))
    user = randomMember
	
	# Creates and returns embed
    embed = discord.Embed(colour=discord.Colour(0x5659e6))
    embed.set_thumbnail(url=user.avatar_url)
	# Uses default avatar if the user has no avatar
    if user.avatar_url == '':
        embed.set_thumbnail(url=user.default_avatar_url)
    embed.add_field(name="Random User", value=randomMember.mention)

    await bot.say(embed=embed)

@bot.command()
async def randomnumber(left=None, right=None):
    # Returns random integer greater than or equal to the first arg and lesser than or equal to the second arg
    """Chooses random number in between two given numbers."""
	
    try:
        await bot.say(random.randint(int(left), int(right)))
	# Returns error message if arguments are invalid
    except:
        await bot.say('You did not pass the required arguments: try again, and this time use `{}randomnumber [number] [number]`'.format(command_prefix))

@bot.command()
async def recipe(*, arg):
	# Returns top 5 recipes from search on food2fork.com, including the thumbnail for the top result
    """Searches for food recipe."""
	
	# Opens client session with food2fork api and retrieves search results
    f2f_url = "http://food2fork.com/api/search?key=d5ce9090bf6b0e4669c8a3bd12e3bf4d&q=" + str(URL(arg))
    session = aiohttp.ClientSession()
    async with session.get(f2f_url) as response:
        data = await response.text()
        data = json.loads(data)
    session.close()

	# Creates and returns embed 
    try:
        embed = discord.Embed(title="Top 5 results for '{}'".format(arg), colour=discord.Colour(0x5659e6))

        embed.set_thumbnail(url=data['recipes'][0]['image_url'])
        embed.set_footer(text="Results taken from food2fork.com", icon_url="https://pbs.twimg.com/profile_images/2954753821/c6a678845d0263172873b01925ee5660_400x400.png")
        for i in range(0,5):
            embed.add_field(name=(html.unescape(data['recipes'][i]['title'])), value=html.unescape("[Recipe from {}]({})".format(data['recipes'][i]['publisher'], data['recipes'][i]['source_url'])), inline=False)
        await bot.say(embed=embed)
	# Returns error message if no results are found or run out of API uses for the day
    except IndexError:
        await bot.say("No results found for '{}'".format(arg))
    except KeyError:
        await bot.say("Reached limit of 50 uses for the day, wait until tomorrow to make more searches")
		
@bot.command()
async def ping():
	# Returns "pong"
	"""Tests server ping"""
	
	await bot.say("Bruh!")
	
classesData = {}

@bot.group(aliases = ['hw'], pass_context = True)
async def homework(ctx):
	"""Commands relating to homework feature."""
	
	if ctx.invoked_subcommand is None:
		await bot.say('Invalid subcommand.')

@homework.command()
async def test():
	await bot.say('lol this is a useless command')
	await bot.say('but if you\'re reading this that means the homework command is working')
	await bot.say('so nice')
	
@homework.group(pass_context = True)
async def classes(ctx):
	"""Commands relating to classes for the homework feature."""
	
	if ctx.invoked_subcommand is None:
		await bot.say('Invalid subcommand.')

@classes.command()
async def test():
	await bot.say('yep it still works, cool')
	
@classes.command()
async def add(*, name : str):
	if name.strip() is '':
		await bot.say('You must provide the name of the class you want to add. Try again, and this time use `{}homework classes add [name]`'.format(command_prefix))
	else:
		classesData[name] = []
		with open('homework.json', 'w') as outfile:
			json.dump(classesData, outfile)
		with open('homework.json', 'r') as infile:
			test = json.loads(infile.read())
			await bot.say(test)
		await bot.say('Successfully added new class "{}".'.format(name))
		
	
bot.run(os.environ.get('token'))