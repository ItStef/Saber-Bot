import discord
from discord.ext import commands

import asyncio
import os
from dotenv import load_dotenv
import subprocess

import wavelink

load_dotenv()

bot = commands.Bot(command_prefix='.', intents = discord.Intents.all(), help_command=None)


@bot.event
async def on_ready():
    try:
        await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='The World Burn'))
    except Exception as e:
        print(e)
    print('Saber online')
    await bot.loop.create_task(setup_hook())

#Loads all cogs
async def load():
    try:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
    except Exception as e:
        print(e)

#Connects to the Lavalink server
async def setup_hook():
    try:
        nodes = [wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')]
        await wavelink.Pool.connect(nodes=nodes, client=bot, cache_capacity=100)
    except Exception as e:
        print(e)
        
#Launches Lavalink server alongside the bot
def launch_music_server():
    try:
        currDir = os.path.dirname(os.path.abspath(__file__))
        serverPath = os.path.join(currDir,'Lavalink.jar')
        subprocess.Popen(['java', '-jar', serverPath])
    except Exception as e:
        print(e)
launch_music_server()


async def main():
    await load()
    await bot.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())