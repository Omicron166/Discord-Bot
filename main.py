from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import Intents
from sys import argv as args
from os.path import isfile
from yt_dlp import YoutubeDL
import json

if isfile('./config.json'):
    path = './config.json'
else:
    path = args[1]

with open(path, 'r') as f:
    config = json.load(f)

intents = Intents().default()
intents.message_content = True

if args[0].endswith('.exe'):
    from discord import opus
    opus.load_opus("opus.dll")

client = commands.Bot(command_prefix=config["prefix"], intents=intents)  # prefix our commands with '.'

#players = {}

@client.event  # check if bot is ready
async def on_ready():
    print('Bot online as', client.user.name)


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
#@client.command()
#async def join(ctx):
#    try:
#        channel = ctx.message.author.voice.channel
#    except AttributeError:
#        await ctx.send('Please join a voice channel')
#        return
#    voice = get(client.voice_clients, guild=ctx.guild)
#    if voice and voice.is_connected():
#        await voice.move_to(channel)
#    else:
#        voice = await channel.connect()


# command to play sound from a youtube URL
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice:
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send('Please join a voice channel')
            return

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    if not voice.is_playing():
        await ctx.send('Trying to play the song')
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

#    if voice.is_playing():
#        voice.stop()
#        await ctx.send('Stopping...')
    await voice.disconnect()


# just a debug command
@client.command()
async def debug(ctx):
    print(opus.is_loaded())

client.run(config["token"])