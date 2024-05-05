import discord
from discord.ext import commands
import aiohttp
import os

api_key = os.getenv('WEATHER_API_KEY')

class Weather(commands.Cog):
    
    def __innit__(self, bot):
        self.bot = bot

    #Weather command
    @commands.command()
    async def weather(self,ctx: commands.Context ,*,city):
        url = 'http://api.weatherapi.com/v1/current.json'
        params={
            'key': api_key,
            'q': city
        }

        #Get the data from the api
        async with aiohttp.ClientSession() as session:
            async with session.get(url,params=params) as res:
                data = await res.json()
                
                #Get the data from the json
                location = data['location']['name']
                temp_c = data['current']['temp_c']
                temp_f = data['current']['temp_f']
                humidity = data['current']['humidity']
                wind_kph = data['current']['wind_kph']
                wind_mph = data['current']['wind_mph']
                condition = data['current']['condition']['text']
                image_url = 'http:' + data['current']['condition']['icon']

                #Embed for the weather
                embed = discord.Embed(title=f'Weather for {location}', description=f'The condition is `{condition}.`', color= discord.Color.yellow())
                embed.add_field(name='Temperature', value=f'{temp_c}°C')
                embed.add_field(name='Humidity', value=f'{humidity}%')
                embed.add_field(name='Wind Speeds', value=f'{wind_kph}kph')
                
                embed.set_thumbnail(url=image_url)
                embed.set_footer(text=f'Requested by {ctx.author.name}')
                await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))