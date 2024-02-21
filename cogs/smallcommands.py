from discord.ext import commands
import random
import discord
import os

class SmallCommands(commands.Cog):
    def __innit__(self, bot):
        self.bot = bot  

    #vs command
    @commands.command()
    async def vs(self, ctx, x, y):
        winner = random.randint(0,1)
        if winner == 1:
            await ctx.reply(x)
        else:
            await ctx.reply(y)

    #coin flip
    @commands.command()
    async def coin(self,ctx):
        coin = random.randint(0, 1)
        if coin == 1:
            await ctx.reply('Heads')
        else:
            await ctx.reply('Tails')
    
    #ping command
    @commands.command()
    async def ping(self,ctx):
        await ctx.send('Pong')



async def setup(bot):
    await bot.add_cog(SmallCommands(bot))
