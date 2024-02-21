from discord.ext import commands
import discord

class Help(commands.Cog):
    def __innit__(self, bot):
        self.bot = bot

    #Help command for general commands
    @commands.command()
    async def help(self,ctx):
        try:
            embed = discord.Embed(title='List of commands:', color= discord.Color.blue())
            
            embed.add_field(name='.help', value='Shows this message.',inline=True)
            embed.add_field(name='.ping', value='Pong',inline=True)
            embed.add_field(name='.coin', value='Flips a coin.', inline=True)
            embed.add_field(name='.execute', value='Kill them.')
            embed.add_field(name='.gaming', value='Saber gaming.',inline=True)
            embed.add_field(name='.reaction', value='Sabers honest reaction to that information.',inline=True)
            embed.add_field(name='.vs [a] [b]', value='Shows which one is objectivally right.',inline=True)
            embed.add_field(name='.size', value='Find out who is bigger.')
            embed.add_field(name='.gamba [amount]', value='Gamble your life saving away.',inline=True)
            embed.add_field(name='.weather [city]', value='Shows weather in the city.',inline=True)
            embed.add_field(name='.helpmusic', value='Get the help menu for music-related commands.', inline= True)

            embed.set_footer(text=f'Requested by {ctx.author.name}')
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.channel.send('An error has occured while trying to send the help message. Please try again later.')

    #Help command for music commands
    @commands.command()
    async def helpmusic(self,ctx):
        try:
            embed = discord.Embed(title='List of music commands:', color= discord.Color.blue())
            
            embed.add_field(name='.play [link/name]/.p [link/name]', value='Plays the song you sent.',inline=True)
            embed.add_field(name='.pause/.resume', value='Pauses or continues the current song.',inline=True)
            embed.add_field(name='.skip/.s', value='Skips current song.',inline=True)
            embed.add_field(name='.queue/.q', value='Shows the queue of the songs.',inline=True)
            embed.add_field(name='.clear/.c', value='Clears the queue.',inline=True)
            embed.add_field(name='.leave/.l/.dc', value='Disconnects the bot.',inline=True)
            embed.add_field(name='.playing', value='Check what song is currently playing.',inline=True)
            embed.add_field(name='.loop [y/n]', value='Loop the queue.',inline=True)
            embed.add_field(name='.shuffle', value='Shuffles the queue.',inline=True)
            embed.add_field(name='.nightcore[on/off]/.nc[on]', value='Enables/disables nightcore mode of the player.',inline=True)
            embed.add_field(name='.remove [songnumber]', value='Remove a specific song in queue.',inline=True)
            
            embed.set_footer(text=f'Requested by {ctx.author.name}')
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.channel.send('An error has occured while trying to send the help music message. Please try again later.')

async def setup(bot):
    await bot.add_cog(Help(bot))