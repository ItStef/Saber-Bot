import discord
from discord import Spotify
from discord.ext import commands
import spotify
import os

#get spotify client and secret from .env
spotifyClientID = os.getenv('SPOTIFY_CLIENT_ID')
spotifyClientSecret = os.getenv('SPOTIFY_CLIENT_SECRET')

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Get the current song the user is listening to
    @commands.command()
    async def listening(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        
        #Get the spotify result
        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

        #If the user is not listening to spotify
        if spotify_result is None:
            await ctx.send(f'{user.name} is not listening to Spotify.')
        
        await ctx.send(f'https://open.spotify.com/track/{spotify_result.track_id}')


async def setup(bot):
    await bot.add_cog(Spotify(bot))