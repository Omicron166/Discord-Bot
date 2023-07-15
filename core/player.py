from discord import Guild
from discord.ext.commands import context, Bot
from discord.utils import get
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class QueuePlayer:
    def __init__(self, client: Bot):
        self.queues = {}
        self.client = client

    def add(self, ctx: context, url: str):
        if not self.queues.get(ctx.guild.id):
            self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(url)

    def play_next(self, ctx: context):
        if len(self.queues.get(ctx.guild.id)) <= 0: return
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if not voice: return

        url = self.queues[ctx.guild.id].pop(0)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        voice.play(FFmpegPCMAudio(info['url'], **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))