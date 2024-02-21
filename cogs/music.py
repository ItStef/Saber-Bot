from discord.ext import commands
import discord
import wavelink
import asyncio
from typing import cast

class Music(commands.Cog):
    def __innit__(self, bot):
        self.bot = bot  

    @commands.Cog.listener() #Confirms node connection
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        print(f'Node {payload.node!r} is ready!')

    
    @commands.command(aliases=['p']) #Play a song or playlist
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)   #Define player
        
        if not player:  #Check if in vc or if discord error
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                await ctx.send('Please join a voice channel first before using this command.')
                return
            except discord.ClientException:
                await ctx.send('I was unable to join this voice channel. Please try again.')
                return
            
        player.autoplay = wavelink.AutoPlayMode.enabled #Enable autoplay

        tracks = wavelink.Search = await wavelink.Playable.search(query) #Search for the track
        if not tracks:  #If no track is found
            await ctx.send('No tracks found with that query. Please try again.')
            return

        try:
            if isinstance(tracks, wavelink.Playlist):  #If the track is a playlist
                added: int = await player.queue.put_wait(tracks)
                await ctx.send(f'Added playlist to the queue.')
            else:                                       #If the track is a song
                track: wavelink.Playable = tracks[0]
                await player.queue.put_wait(track)
                await ctx.send(f'Added {track.title} to the queue.')
        except Exception as e:
            print(e)
            await ctx.send('An error has occured while trying to play the song. Please try again later.')
            return

        if not player.playing:  #Plays the song
            await player.play(player.queue.get())

    @commands.command(aliases=['np']) #Shows the song currently being played
    async def playing(self, ctx):
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        if player.playing:
            embed = discord.Embed(title='Now playing:', color= discord.Color.blue())
            embed.add_field(name=f'{player.current.title}', value=f'by {player.current.author}', inline=True)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.send('Nothing is being played right now.')
            await ctx.message.add_reaction('\u274E')


    @commands.command(aliases=['s']) #Skips the current song in queue
    async def skip(self, ctx):
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        if player.playing:
            await player.skip(force=True)
            await ctx.message.add_reaction('\u2705')    #positive square
        else:
            await ctx.send('There is nothing to skip')
            await ctx.message.add_reaction('\u274E')    #negative square


    @commands.command(aliases=['pause', 'resume'])  #Pause or Resume the Player depending on its current state
    async def pause_resume(self, ctx) -> None:
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        await player.pause(not player.paused)
        await ctx.message.add_reaction('\u2705')


    @commands.command(aliases=['nc']) #Option to turn the player into nightcore mode
    async def nightcore(self, ctx, switch: str) -> None:
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return
 
        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        filters: wavelink.Filters = player.filters
        match switch:
            case 'on':
                filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
                await player.set_filters(filters)
                await ctx.send('Nightcore mode has been set to on.')
            case 'off':
                filters.timescale.set(pitch=1, speed=1, rate=1)
                await player.set_filters(filters)
                await ctx.send('Nightcore mode has been set off.')
            case _:
                await ctx.send('Invalid mode. Please use either on or off.')

        await ctx.message.add_reaction('\u2705')
    

    @commands.command(aliases=['c']) #Clears the queue
    async def clear(self, ctx):
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        player.queue.clear()
        await ctx.send('Queue has been cleared.')
        await ctx.message.add_reaction('\u2705')


    @commands.command() #Shuffles the queue
    async def shuffle(self, ctx):
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        player.queue.shuffle()
        await ctx.send('Queue has been shuffled.')
        await ctx.message.add_reaction('\u2705')


    @commands.command() #Loops the queue
    async def loop(self, ctx, mode: str):
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        match mode:
            case 'y':
                player.queue.mode = wavelink.QueueMode.loop
                await ctx.send('Queue is being looped.')
            case 'n':
                player.queue.mode = wavelink.QueueMode.normal
                await ctx.send('Queue is not being looped anymore.')
            case _:
                await ctx.send('Not a valid mode.')
        await ctx.message.add_reaction('\u2705')


    @commands.command(aliases=['q']) #Shows the queue of the songs
    async def queue(self, ctx):
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        
        embed = discord.Embed(title='Queue:', color= discord.Color.blue())
        song_counter = 0

        for song in player.queue:
            song_counter += 1
            try: 
                artistOrAuthor = song.author
            except AttributeError: 
                artistOrAuthor = song.artist
            #Embed making
            if song_counter % 25 == 0 and song_counter > 0:  # If song counter is a multiple of 25 and not 0, send the current embed and create a new one
                await ctx.send(embed=embed)
                embed = discord.Embed(title='Queue:')

            if song_counter != 0:  # Add the song to the embed, unless it's the first song (since the first embed is empty)
                embed.add_field(name=f'[{song_counter}] {song.title}', value=song.author, inline=False)

        if song_counter == 0:
            await ctx.send('The queue is currently empty.')
        else:
            await ctx.send(embed = embed)


    @commands.command(aliases=['rm']) #Remove specific song from queue
    async def remove(self,ctx, query: int) -> None:
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return

        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        #Check if the queue is empty or if the query is invalid
        if not player.queue or query <= 0 or query > len(player.queue):
            await ctx.send('Invalid query. Please try again.')
            return
        else:#Remove the song from the queue
            await ctx.send(f'Removed **{player.queue.peek(query-1)}** from queue!')
            player.queue.delete(query-1)


    @commands.command(aliases=['dc','leave','l']) #Disconnect from the current voice channel
    async def disconnect(self, ctx) -> None:    
        if not ctx.voice_client:
            await ctx.send('I am not currently in a voice channel.')
            return
        
        try:
            player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        except AttributeError:
            await ctx.send('Failed to cast voice client to player.')
            return
        #Clear the queue and disconnect
        player.queue.clear()
        await ctx.voice_client.disconnect()

        await ctx.send('Sayonaraaaa..')
        await ctx.message.add_reaction('\u2705')


async def setup(bot):
    await bot.add_cog(Music(bot))