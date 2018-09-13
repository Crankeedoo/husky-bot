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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def litty():
    for i in range(5):
        await bot.say('litty' + i*'!')
        time.sleep(2)

@bot.command()
async def miles():
    for i in range(100):
        await bot.say('<@!288500929400143873>')

@bot.command()
async def coin():
    # &coin
    # Flips a coin
    """Flips a coin."""
    if random.randint(1,2) == 1:
        await bot.say('Your coin came up heads.')
    else:
        await bot.say('Your coin came up tails.')

@bot.command(pass_context = True)
async def randomuser(ctx):
    # Chooses random user from server, mentions them and posts their avatar in an embed
    """Selects a random user from the server."""
    server = ctx.message.server
    message = ctx.message
    randomMember = random.choice(list(server.members))
    user = randomMember
    embed = discord.Embed(colour=discord.Colour(0x5659e6))
    embed.set_thumbnail(url=user.avatar_url)
    if user.avatar_url == '':
        # Uses default avatar if the user has no avatar
        embed.set_thumbnail(url=user.default_avatar_url)
    embed.add_field(name="Random User", value=randomMember.mention)

    await bot.say(embed=embed)

@bot.command()
async def randomnumber(left=None, right=None):
    # Chooses integer larger than the first arg and smaller than the second
    """Chooses random number in between two given numbers"""
    try:
        await bot.say(random.randint(int(left), int(right)))
    except:
        await bot.say('You did not pass the required arguments: try again, and this time use `' + command_prefix + 'randomnumber [number] [number]`')

@bot.command()
async def recipe(*, arg):
    """Searches for recipe"""
    f2f_url = "http://food2fork.com/api/search?key=d5ce9090bf6b0e4669c8a3bd12e3bf4d&q=" + str(URL(arg))
    session = aiohttp.ClientSession()
    async with session.get(f2f_url) as response:
        data = await response.text()
        data = json.loads(data)
    session.close()

    try:
        embed = discord.Embed(title="Top 5 results for '{}'".format(arg), colour=discord.Colour(0x5659e6))

        embed.set_thumbnail(url=data['recipes'][0]['image_url'])
        embed.set_footer(text="Results taken from food2fork.com", icon_url="https://pbs.twimg.com/profile_images/2954753821/c6a678845d0263172873b01925ee5660_400x400.png")
        for i in range(0,5):
            embed.add_field(name=(html.unescape(data['recipes'][i]['title'])), value=html.unescape("[Recipe from {}]({})".format(data['recipes'][i]['publisher'], data['recipes'][i]['source_url'])), inline=False)
        await bot.say(embed=embed)
    except IndexError:
        await bot.say("No results found for '{}'".format(arg))
    except KeyError:
        await bot.say("Reached limit of 50 uses for the day, wait until tomorrow to make more searches")

bot.run(os.environ.get('token'))
