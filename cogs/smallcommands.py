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
        try:
            winner = random.randint(0,1)
            if winner == 1:
                await ctx.reply(x)
            else:
                await ctx.reply(y)
        except:
            await ctx.reply('Invalid input')

    #coin flip
    @commands.command()
    async def coin(self,ctx):
        try:
            coin = random.randint(0, 1)
            if coin == 1:
                await ctx.reply('Heads')
            else:
                await ctx.reply('Tails')
        except:
            await ctx.reply('Invalid input')

    #8ball command
    @commands.command()

    async def eightball(self,ctx,*,question):
        try:
            responses = ['It is certain.',
                        'It is decidedly so.',
                        'Without a doubt.',
                        'Yes - definitely.',
                        'You may rely on it.',
                        'As I see it, yes.',
                        'Most likely.',
                        'Outlook good.',
                        'Yes.',
                        'Signs point to yes.',
                        'Reply hazy, try again.',
                        'Ask again later.',
                        'Better not tell you now.',
                        'Cannot predict now.',
                        'Concentrate and ask again.',
                        "Don't count on it.",
                        'My reply is no.',
                        'My sources say no.',
                        'Outlook not so good.',
                        'Very doubtful.']
            await ctx.reply(f'Question: {question}\nAnswer: {random.choice(responses)}')
        except:
            await ctx.reply('Invalid input')

    #ping command
    @commands.command()
    async def ping(self,ctx):
        await ctx.send('Pong')


async def setup(bot):
    await bot.add_cog(SmallCommands(bot))
