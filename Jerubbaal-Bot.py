import discord
from discord.ext import commands
import asyncio
from mutagen.mp3 import MP3
import mutagen
import math
import os

TOKEN_NAME = "JERUBBAAL_TOKEN"

PREFIX = "jerubbaal"

PLAY_AUDIO_FILES = {"ttsing": r"C:\Users\royat\Desktop\ttsing.mp3",
                    "moyal": r"E:\Downloads\moyal.mp3",
                    "wontdefeat": r"E:\Downloads\wontdefeat.mp3",
                    "shira": r"D:\Downloads\shira.mp3",
                    "cohen": r"C:\Users\royat\Documents\Sound recordings\cohen.m4a",
                    "bruh": r"D:\Downloads\Bruh Sound Effect #2.mp3"}

bot = commands.Bot(command_prefix=f"{PREFIX} ")


def error_str(err):
    return "Error: " + err


class Jerobaal(commands.Cog):
    def __init__(self, cog_bot):
        self.bot = cog_bot
        self._last_member = None
        self.voice_client = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.message.reply("זרע עלמק?")

    @commands.command()
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        if voice_channel is not None:
            self.voice_client = await voice_channel.connect()

    @commands.command()
    async def goodnight(self, ctx):
        if ctx.author.voice.channel is None:
            await ctx.send("You must be in a voice channel in order to run this command")
        vc_members = ctx.guild.get_channel(ctx.author.voice.channel.id).voice_states
        print(vc_members.keys())
        for mem in vc_members.keys():
            d = ctx.guild.get_member(mem)
            print(d)
            if d is None:
                continue
            # await mem.edit(voice_channel=None)
            print(f"would kick {ctx.guild.get_member(mem).name}")

    @commands.command(aliases=["pa"], help="Play an audio from selected list",
                      name="playaudio")
    async def play_audio(self, ctx, audio, repeat=1):
        channel = ctx.author.voice
        if channel is None:
            raise commands.ChannelNotFound
        channel = channel.channel
        if audio == "list":
            list_str = "Available sounds:\n"
            for audio_file in PLAY_AUDIO_FILES.keys():
                list_str += f"\t- {audio_file}\n"
            await ctx.message.reply(list_str + "\n")
            return
        if audio not in PLAY_AUDIO_FILES.keys() or not os.path.isfile(PLAY_AUDIO_FILES[audio]):
            raise commands.BadArgument

        if ctx.guild.voice_client is None and (ctx.guild.get_member(ctx.bot.user.id).voice is None or
                                               ctx.guild.get_member(ctx.bot.user.id).voice.channel is None):
            await channel.connect()

        length = math.ceil(MP3(PLAY_AUDIO_FILES[audio]).info.length)
        for _ in range(repeat):
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(PLAY_AUDIO_FILES[audio]), after=self.actual_play_audio)
            await asyncio.sleep(length)
        await ctx.guild.voice_client.disconnect()

    @staticmethod
    def actual_play_audio(error):
        if error is not None:
            print(error)

    @play_audio.error
    async def play_audio_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing audio file!"))
        elif isinstance(error, commands.BadArgument):
            await ctx.message.reply(error_str("file doesn't exist"))
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.message.reply(error_str("you must be in a voice channel in order to run this command"))
        else:
            print(error)
            if ctx.guild.voice_client is not None:
                ctx.guild.voice_client.disconnect()

    @commands.command()
    async def clear(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit+1, check=lambda msg: msg != ctx.message)
        await ctx.send(f"Cleared {limit} messages!")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing amount"))
        else:
            print(error)

    # @commands.command()
    # async def help(self, ctx):
    #     await ctx.message.reply(HELP_CMD)

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.message.reply(error_str("missing argument"))

    @commands.Cog.listener()
    async def on_connect(self):
        print(f"Connected as {self.bot.user}")

    # @commands.Cog.listener()
    # async def on_message(self, msg):
    #     await msg.reply(HELP_CMD)


tokens = open(r"..\tokens.txt", "r")
token = ""
for line in tokens.readlines():
    splitted = line.split('=')
    if splitted[0] == TOKEN_NAME:
        token = splitted[1]
if token == "":
    print("File tokens.txt not found!")
    exit(1)


bot.add_cog(Jerobaal(bot))
bot.intents.all()
bot.run(token)
