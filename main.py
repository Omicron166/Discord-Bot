from discord.ext import commands
from discord.utils import get
from discord import Intents
from sys import argv as args
from os.path import isfile
from yt_dlp import YoutubeDL
from core.player import QueuePlayer
from discord import opus
import json

YDL_OPTIONS = {
    'format': 'bestaudio', 'noplaylist': 'True'
}

if isfile('./config.json'):
    path = './config.json'
else:
    path = args[1]

with open(path, 'r') as f:
    config = json.load(f)

intents = Intents().default()
intents.message_content = True

if config['bundle']:
    print('Trying to load opus from dll')
    opus.load_opus("opus.dll")

client = commands.Bot(command_prefix=config["prefix"], intents=intents)  # prefix our commands with '.'

queue = QueuePlayer(client)

@client.event  # check if bot is ready
async def on_ready():
    print('Bot online as', client.user.name)


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@client.command()
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        await ctx.send('Please join a voice channel')
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@client.command()
async def play(ctx, url):
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
    try:
        await ctx.send('Parsing url')
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    except:
        await ctx.send('Invalid url')
        return

    queue.add_song(ctx, info)
    if not voice.is_playing():
        queue.play_next(ctx)

    # check if the bot is already playing
    else:
        await ctx.send(f'Song "{info["title"]}" added to queue')

#https://www.youtube.com/watch?v=ISNP9UgeQ0I
@client.command()
async def loop(ctx, url):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice: voice.disconnect()
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        await ctx.send('Please join a voice channel')
        return
    voice = await channel.connect()

    try:
        await ctx.send('Parsing url')
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    except:
        await ctx.send('Invalid url')
        return
    
    queue.del_queue(ctx)
    queue.loop_song(ctx, info)
    await ctx.send('Now looping: ' + info['title'])

@client.command()
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice: return
    if voice.is_playing(): 
        voice.stop()
        await ctx.send("Song skipped")

# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Resuming music')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Music paused')


# command to stop voice
@client.command()
async def stop(ctx):
    queue.del_queue(ctx)
    voice = get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()


# just a debug command
@client.command()
async def debug(ctx):
    print(opus.is_loaded())

@client.event
async def on_voice_state_update(member, before, after):
    # Verificar si el miembro afectado no es el bot
    if member != client.user:
        # Verificar si el bot se ha desconectado del canal de voz actual
        if before.channel and not after.channel and before.channel == member.guild.voice_client.channel:
            # Verificar si no hay otros miembros en el canal de voz antes de desconectar
            if len(before.channel.members) == 1:
                voice_client = client.voice_clients[0]
                if voice_client and voice_client.is_connected():
                    await voice_client.disconnect()


client.run(config["token"])