from discord.ext import commands
import discord
from discord.ext.commands.core import command
import youtube_dl

class music(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("**You must be connected to a voice channel to use this command.**")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send(f"*Successfully connected to: {voice_channel}*")
        else:
            if len(ctx.voice_client.channel.members) == 1:
                await ctx.voice_client.move_to(voice_channel)
                await ctx.send(f"*Successfully connected to: {voice_channel}*")
            else:
                await ctx.send("**Someone else is already listening to music in different channel.**")

    @commands.command(aliases=['dc'])
    async def disconnect(self,ctx):
        voice = ctx.voice_client

        if ctx.author.voice is None:
            await ctx.send("**You must be connected to a voice channel to use this command.**")
        elif ctx.voice_client is None:
            await ctx.send("**I'm not in a voice channel.**")
        else:
            if ctx.author.voice.channel == voice.channel:
                await ctx.voice_client.disconnect()
                await ctx.send(f"*Successfully disconnected from: {voice.channel}*")
            else:
                if len(ctx.voice_client.channel.members) == 1:
                    await ctx.voice_client.disconnect()
                    await ctx.send(f"*Successfully disconnected from: {voice.channel}*")
                else:
                    await ctx.send("**Someone else is already listening to music in different channel.**")

    @commands.command(aliases=['p'])
    async def play(self,ctx,url):
        voice = ctx.voice_client

        if ctx.author.voice is None:
            await ctx.send("**You must be connected to a voice channel to use this command.**")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
            YDL_OPTIONS = {'format':'bestaudio'}
            
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
                ctx.voice_client.play(source)
        else:
            if ctx.author.voice.channel == voice.channel:
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
                YDL_OPTIONS = {'format':'bestaudio'}

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
                    ctx.voice_client.play(source)
            else:
                if len(ctx.voice_client.channel.members) == 1:
                    await ctx.voice_client.move_to(voice_channel)
                    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
                    YDL_OPTIONS = {'format':'bestaudio'}

                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url, download=False)
                        url2 = info['formats'][0]['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
                        ctx.voice_client.play(source)
                else:
                    await ctx.send("**Someone else is already listening to music in different channel.**")

    @commands.command()
    async def pause(self,ctx):
        voice = ctx.voice_client

        if ctx.author.voice is None:
            await ctx.send("**You must be connected to a voice channel to use this command.**")
        elif ctx.voice_client is None:
            await ctx.send("**I'm not in a voice channel.**")
        else:
            if ctx.author.voice.channel == voice.channel:
                if ctx.voice_client.is_playing():
                    ctx.voice_client.pause()
                    await ctx.send("*Successfully paused the song.*")
                elif ctx.voice_client.is_paused():
                    await ctx.send("**I'm already paused.**")
                else:
                    await ctx.send("**Nothing is playing.**")
            else:
                await ctx.send("**Someone else is already listening to music in different channel.**")

    @commands.command()
    async def resume(self,ctx):
        voice = ctx.voice_client

        if ctx.author.voice is None:
            await ctx.send("**You must be connected to a voice channel to use this command.**")
        elif ctx.voice_client is None:
            await ctx.send("**I'm not in a voice channel.**")
        else:
            if ctx.author.voice.channel == voice.channel:
                if ctx.voice_client.is_paused():
                    ctx.voice_client.resume()
                    await ctx.send("*Successfully resumed the song.*")
                elif ctx.voice_client.is_playing():
                    await ctx.send("**Music is already playing.**")
                else:
                    await ctx.send("**Nothing is playing.**")
            else:
                await ctx.send("**Someone else is already listening to music in different channel.**")

    @commands.command()
    async def stop(self,ctx):
        voice = ctx.voice_client

        if ctx.author.voice is None:
            await ctx.send("**You must be connected to a voice channel to use this command.**")
        elif ctx.voice_client is None:
            await ctx.send("**I'm not in a voice channel.**")
        else:
            if ctx.author.voice.channel == voice.channel:
                if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                    ctx.voice_client.stop()
                    await ctx.send("*Successfully stopped the song.*")
                else:
                    await ctx.send("**Nothing is playing.**")
            else:
                await ctx.send("**Someone else is already listening to music in different channel.**")
        
def setup(client):
    client.add_cog(music(client))