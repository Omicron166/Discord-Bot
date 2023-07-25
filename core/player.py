from discord.ext.commands import context, Bot
from discord.utils import get
from discord import FFmpegPCMAudio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class QueuePlayer:
    def __init__(self, client: Bot):
        self.queues = {}
        self.client = client

    def add(self, ctx: context, info: dict):
        if not self.queues.get(ctx.guild.id):
            self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(info)

    def get_queue(self, ctx: context):
        if not self.queues.get(ctx.guild.id): return []
        return self.queues[ctx.guild.id]
    
    def del_queue(self, ctx: context):
        del self.queues[ctx.guild.id]

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
        voice.play(FFmpegPCMAudio(info['url'], **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))