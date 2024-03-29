from discord.ext import commands
import discord

class Greetings(commands.Cog):  #welcome message
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            channel = member.guild.system_channel
            if channel is not None:
                await channel.send(f'Welcome {member.mention}')
        except Exception as e:
            print(e)
            print('Error in on_member_join')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        #Says hello to the user
        try:
            member = member or ctx.author
            if self._last_member is None or self._last_member.id != member.id:
                await ctx.send(f'Hello {member.name}~')
            else:
                await ctx.send(f'Hello {member.name}... This feels familiar.')
            self._last_member = member
        except Exception as e:
            print(e)
            await ctx.channel.send('An error has occured while trying to say hello. Please try again later.')

async def setup(bot):
    await bot.add_cog(Greetings(bot))