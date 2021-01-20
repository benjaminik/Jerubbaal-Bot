import discord
from discord.ext import commands
import time

TOKEN = ""
#TOKEN = "fjxvcCItq-przRba2gdu_F1FeDbbis6T"
#MEITAV_TOKEN = 'NjkwMjI0MTYwMjQ4NjkyNzYw.XnOd7g.YAwytPJ6Y40T5OUgtgZgD5sNvC8'
#YEROBAAL_TOKEN = 'ODAwNDYxNTA2OTQwMTA4ODUw.YASd3w.J2Yow1a6y90Yu6Fa_p0MwzrCPIk'

PREFIX = "jerobaal"

PLAY_AUDIO_FILES = {"ttsing": r"C:\Users\royat\Desktop\ttsing.mp3",
                    "moyal": r"E:\Downloads\moyal.mp3",
                    "wontdefeat": r"E:\Downloads\wontdefeat.mp3",
                    "shira": r"D:\Downloads\shira.mp3",
                    "cohen": r"C:\Users\royat\Documents\Sound recordings\cohen.m4a",
                    "bruh": r"D:\Downloads\Bruh Sound Effect #2.mp3"}

bot = commands.Bot(command_prefix=f"{PREFIX} ")

HELP_CMD = "tambal"


def error_str(err):
    return "Error: " + err


class Jerobaal(commands.Cog):
    def __init__(self, cog_bot):
        self.bot = cog_bot
        self._last_member = None
        self.voice_client = None
        self.repeat_num = 0
        self.audio_file = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.message.reply("שלום וברוכים הבאים למרכז השירות של צהל")

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
        if audio not in PLAY_AUDIO_FILES.keys():
            raise commands.BadArgument

        if ctx.guild.voice_client is None or ctx.guild.get_member(ctx.bot.user.id).voice is None or \
                ctx.guild.get_member(ctx.bot.user.id).voice.channel is None:
            await channel.connect()

        self.repeat_num = repeat
        self.audio_file = audio
        self.actual_play_audio(None)
        ctx.guild.voice_client.play(discord.FFmpegPCMAudio(PLAY_AUDIO_FILES[self.audio_file]),
                                    after=self.actual_play_audio)
        # await ctx.guild.voice_client.disconnect()

    def actual_play_audio(self, error):
        return
        if error is not None:
            print(error)
        if self.repeat_num == 0:
            return -1
        self.repeat_num -= 1

    @play_audio.error
    async def play_audio_error(self, ctx, error):
        usage = "Usage: jerobaal playaudio [audio (or list)] <repeat amount>"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing audio file!\n" + usage))
        elif isinstance(error, commands.BadArgument):
            await ctx.message.reply(error_str("file doesn't exist\n" + usage))
        elif isinstance(error, commands.ChannelNotFound):
            print("no channel")
            await ctx.message.reply(error_str("you must be in a voice channel in order to run this command"))
        else:
            print(error)

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


tokens = open("tokens.txt", "r")
for line in tokens.readlines():
    splitted = line.split('=')
    if splitted[0] == "JERUBBAAL_TOKEN":
        TOKEN = splitted[1]
if TOKEN == "":
    exit(1)


bot.add_cog(Jerobaal(bot))
bot.intents.all()
bot.run(TOKEN)
