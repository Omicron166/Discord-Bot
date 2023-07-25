from discord.ext.commands import context, Bot
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Loop:
    def __init__(self, value) -> None:
        self.value = value
        self.is_loop = True
    
    def __len__(self):
        return 1

    def pop(self, index = 0):
        return self.value

class QueuePlayer:
    def __init__(self, client: Bot):
        self.queues = {}
        self.client = client

    def add_song(self, ctx: context, info: dict):
        if not self.queues.get(ctx.guild.id):
            self.create_queue(ctx)
        self.queues[ctx.guild.id].append(info)

    def loop_song(self, ctx: context, info: dict):
        loop = Loop(info)
        self.del_queue(ctx)
        self.queues[ctx.guild.id] = loop
        self.play_next(ctx)

    def get_queue(self, ctx: context):
        if not self.queues.get(ctx.guild.id): return []
        return self.queues[ctx.guild.id]
    
    def create_queue(self, ctx: context):
        self.queues[ctx.guild.id] = []

    def del_queue(self, ctx: context):
        try: del self.queues[ctx.guild.id]
        except: pass

    def play_next(self, ctx: context):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if not voice:
            self.del_queue(ctx)
            return

        if len(self.queues.get(ctx.guild.id)) <= 0:
            self.del_queue(ctx)
            voice.disconnect()
            return

        info = self.queues[ctx.guild.id].pop(0)
        asyncio.get_event_loop().create_task(ctx.send('Now playing: ' + info['title']))
        voice.play(FFmpegPCMAudio(info['url'], **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))