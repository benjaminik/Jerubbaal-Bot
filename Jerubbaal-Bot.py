import inspect
import string

import discord
from discord.ext import commands
import asyncio
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.wave import WAVE
import mutagen
import math
import os
import random
import requests
import json

TOKEN_NAME = "JERUBBAAL_TOKEN"

# PLAY_AUDIO_PATH = r"..\audio" + "\\"
# PLAY_AUDIO_FILES = {"alabama": PLAY_AUDIO_PATH + r"alabama.mp3",
#                     "bruh": PLAY_AUDIO_PATH + r"Bruh Sound Effect #2.mp3",
#                     "cohen": PLAY_AUDIO_PATH + r"cohen.m4a",
#                     "dayan": PLAY_AUDIO_PATH + r"dayan.mp3",
#                     "globglib": PLAY_AUDIO_PATH + r"globglib.mp3",
#                     "hellnaw": PLAY_AUDIO_PATH + r"Oh Hell No #VINE.mp3",
#                     "heysisters": PLAY_AUDIO_PATH + r"heysisters.mp3",
#                     "imgood": PLAY_AUDIO_PATH + r"I’m Good Bruh You Geekin Bruh (192 kbps).mp3",
#                     "moyal": PLAY_AUDIO_PATH + r"moyal.mp3",
#                     "moyal2": PLAY_AUDIO_PATH + r"moyal2.mp3",
#                     "moyal3": PLAY_AUDIO_PATH + r"moyal3.mp3",
#                     "moyalrap": PLAY_AUDIO_PATH + r"moyal_rap.m4a",
#                     "purim": PLAY_AUDIO_PATH + r"purim.mp3",
#                     "shira": PLAY_AUDIO_PATH + r"shira.mp3",
#                     "stepbro": PLAY_AUDIO_PATH + r"stepbro.mp3",
#                     "ttsing": PLAY_AUDIO_PATH + r"ttsing.mp3",
#                     "wontdefeat": PLAY_AUDIO_PATH + r"musc.wav"}
DEFAULT_CURRENTSONG = "song.mp3"
PLAY_AUDIO_PATH = r"https://drive.google.com/uc?export=download&id="
PLAY_AUDIO_FILES = {"alabama": PLAY_AUDIO_PATH + r"1Szlw3aQWPFzAc4EXjoDc1ZIARqtLFbj1",
                    "arielogen": PLAY_AUDIO_PATH + r"1WdoQaXqjDdtqmLead9sOMBpNe_W0UhJD",
                    "benjaminogen": PLAY_AUDIO_PATH + r"1FhQfa4pY33jslRoOBrRm6Tfs0xB02Wh9",
                    "bruh": PLAY_AUDIO_PATH + r"1CPnEc0_8P4yNbLacQHz7OLNPKqmyVUlW",
                    "cohen": PLAY_AUDIO_PATH + r"1DQALe7QpigJzeN6nFLnwJQsu2QFu9m0w",
                    "chupapi": PLAY_AUDIO_PATH + r"1oFRB0mk9ixb2LmcbEFlsCUSwbSc5sIEt",
                    "dayan": PLAY_AUDIO_PATH + r"1TSBrK3EL1aUQZeQif4TWKspwhgoLnqyI",
                    "globglib": PLAY_AUDIO_PATH + r"1_9Em5QiOk6P3hQnrvsZfaUHqW_OfrORc",
                    "hellnaw": PLAY_AUDIO_PATH + r"11410Nl1lghF2XpA51fhsiYjwaM31CxZ3",
                    "heysisters": PLAY_AUDIO_PATH + r"18NxjwyaTsixirWkpmizCS_sRfYEe_EvE",
                    "idoogen": PLAY_AUDIO_PATH + r"1WfgneI1Vcm5PMb47_0MENwsQfmsA5K_1",
                    "imgood": PLAY_AUDIO_PATH + r"1bIPGLBukEylJW-vOvNlIn-XHCVq9mFMT",
                    "moyal": PLAY_AUDIO_PATH + r"18fmO5glKSUbSbwX1kDLjWf216wPu6FiO",
                    "moyal2": PLAY_AUDIO_PATH + r"1oYslu8Ig27jq2bRQQMk1KjLdMIVn_aJq",
                    "moyal3": PLAY_AUDIO_PATH + r"1m8CsGICX2IQ91uqDQbdDdep6Oe_RhH2b",
                    "moyalrap": PLAY_AUDIO_PATH + r"1ubqLkIJxsmQxeQMl3cA9o6V62iUkkXXF",
                    "munyanyu": PLAY_AUDIO_PATH + r"1qYdWwqfrk3MAmFeYc_fwspWRH10p2KfN",
                    "ofekogen": PLAY_AUDIO_PATH + r"1jhZkqLCmGEE6I70UZWzzMYZ_9KnSFh0x",
                    "purim": PLAY_AUDIO_PATH + r"1Wyrk7CqD0CszcjnazKCAwX2b7z-go4Pa",
                    "royogen": PLAY_AUDIO_PATH + r"16J0KuGf2e_dxJcnPJQu1FH-dARlPmamj",
                    "shira": PLAY_AUDIO_PATH + r"1bn6s4VT5AtSDuunOxIc5uH1_JiwOlFuD",
                    "shonogen": PLAY_AUDIO_PATH + r"1yLofhA4pgNGzjvUtXzErwv5lj7E9aPcG",
                    "stepbro": PLAY_AUDIO_PATH + r"1fGk_Dg7KqCuzEsI1VcpLO7vCriB1eIKP",
                    "ttsing": PLAY_AUDIO_PATH + r"16PZRpUlThMwjQBkVYWSl79VwCRbetAf7",
                    "wontdefeat": PLAY_AUDIO_PATH + r"1onzsBINx1cyC2E-IP2PpykPsU5bpsAGm"}

SEND_FILE_PATH = r"..\files" + "\\"
SEND_FILE_FILES = {"ariel": SEND_FILE_PATH + r"ariel.png"}
OWNER_ID = 0

bot = commands.Bot(command_prefix=(f"jerubbaal ", "j ", "chupapi "), intents=discord.Intents.all())
bot.remove_command("help")
bot_owner = discord.User


def error_str(err):
    return "Error: " + err


def audio_len(file):
    ret = 0
    if file.lower().endswith("mp3"):
        ret = math.ceil(mutagen.mp3.MP3(file).info.length)
    if file.lower().endswith("mp4") or file.lower().endswith("m4a"):
        ret = math.ceil(mutagen.mp4.MP4(file).info.length)
    if file.lower().endswith("wav"):
        ret = math.ceil(mutagen.wave.WAVE(file).info.length)
    return ret


class Jerubbaal(commands.Cog):
    def __init__(self, cog_bot):
        self.bot = cog_bot
        self._last_member = None
        self.playing = False
        self.audio = None
        self.aliases = {}
        self.members_kicked = {}

    @staticmethod
    async def unhandled_error(ctx, error):
        error_msg = f"Hey {bot_owner.name}!\n" \
                    f"Sorry to bother you but I had an error :(\n" \
                    f"Anyways, on the `{ctx.guild.name}` ({ctx.guild.id}) guild " \
                    f"this dude `{ctx.author.name}` ({ctx.author.id}) used the command:\n" \
                    f"```{ctx.message.content}```\n" \
                    f"And I got an error of type `{type(error)}` which says:\n" \
                    f"```{error}```\n" \
                    f"{bot_owner.name}, pls fix"
        await bot_owner.send(error_msg)

    @commands.command(aliases=["gn"], help="Disconnects everyone from your channel simultaneously")
    async def goodnight(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You must be in a voice channel in order to run this command")
        vc_members = ctx.author.voice.channel.members
        if len(vc_members) == 0:
            for k in ctx.author.voice.channel.voice_states.keys():
                vc_members.append(await ctx.guild.fetch_member(k))
        for mem in vc_members:
            if mem is None:
                continue
            await mem.edit(voice_channel=None)
        await ctx.message.add_reaction("😴")

    @commands.command(aliases=["pc"], usage="[<members>,...]", help="Creates a private channel just for you and who you tagged!")
    async def privatechannel(self, ctx, *members: discord.Member):
        if len(members) == 0:
            raise commands.MissingRequiredArgument(inspect.Parameter("member", inspect.Parameter.POSITIONAL_ONLY))
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
        for member in members:
            overwrites[member] = discord.PermissionOverwrite(view_channel=True)
        channel_name = f"{ctx.author.nick}'s private channel"
        for p in string.punctuation:
            channel_name = channel_name.replace(p, "")
        channel_name = channel_name.replace(" ", "-").lower()
        if channel_name in [c.name for c in ctx.guild.text_channels]:
            await ctx.message.reply(error_str("You already have a private channel!"))
            return
        new_channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
        welcome_message = await new_channel.send(f"Welcome to <@{ctx.author.id}>'s private channel with "
                                                 f"{','.join([f'<@{m.id}>' for m in members])}!\nYou have 5 minutes!")
        await welcome_message.add_reaction("✅")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅"

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            await new_channel.delete()
        else:
            await new_channel.delete()

    @privatechannel.error
    async def privatechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("you must have at least one member"))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.reply(error_str("member not found"))
        else:
            await Jerubbaal.unhandled_error(ctx, error)

    @commands.command(aliases=["pa", "play"], help="Plays an audio from a predetemined list",
                      name="playaudio", usage="<sound> [repeat]")
    async def play_audio(self, ctx, audio, repeat=1):
        channel = ctx.author.voice
        if channel is None or channel.channel is None:
            await ctx.message.reply(error_str("you must be in a voice channel in order to run this command"))
            return
        channel = channel.channel
        if audio == "list":
            list_str = "Available sounds:\n"
            for audio_file in PLAY_AUDIO_FILES.keys():
                list_str += f"\t- {audio_file}\n"
            await ctx.message.reply(list_str + "\n")
            return
        if audio == "stop":
            if ctx.guild.voice_client is not None:
                ctx.guild.voice_client.stop()
                await ctx.guild.voice_client.disconnect()
            while os.path.isfile(self.audio + ".mp3"):
                try:
                    os.remove(self.audio + ".mp3")
                except PermissionError:
                    continue
            self.audio = None
            self.playing = False
            return
        if audio not in PLAY_AUDIO_FILES.keys():
            await ctx.message.reply(error_str("file doesn't exist"))
            return

        if self.playing:
            await ctx.message.reply(error_str("bot already playing!"))
            return
        if ctx.guild.voice_client is None and (ctx.guild.get_member(ctx.bot.user.id).voice is None or
                                               ctx.guild.get_member(ctx.bot.user.id).voice.channel is None):
            await channel.connect()

        self.audio = audio
        print("Writing")
        with open(audio + ".mp3", "wb") as f:
            f.write(requests.get(PLAY_AUDIO_FILES[audio]).content)
        print("Playing")
        length = audio_len(audio + ".mp3")
        for _ in range(repeat):
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(audio + ".mp3"))
            self.playing = True
            await asyncio.sleep(length)
        os.remove(self.audio + ".mp3")
        self.audio = None
        self.playing = False
        if ctx.guild.voice_client is not None:
            await ctx.guild.voice_client.disconnect()
        await ctx.message.add_reaction("🎶")

    @play_audio.error
    async def play_audio_error(self, ctx, error):
        self.playing = False
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing audio file!"))
        else:
            await Jerubbaal.unhandled_error(ctx, error)
            if ctx.guild.voice_client is not None:
                await ctx.guild.voice_client.disconnect()
            if os.path.isfile(self.audio + ".mp3"):
                os.remove(self.audio + ".mp3")
                self.audio = None

    @commands.command(usage="<amount>", help="Clears the last <amount> messages")
    async def clear(self, ctx, limit: int):
        if limit > 100 or limit < 1:
            await ctx.message.reply(error_str("amount must be an integer between 1 and 100"))
            return
        await ctx.channel.purge(limit=limit+1, check=lambda msg: msg != ctx.message)
        await ctx.message.add_reaction("👍🏻")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing amount"))
        elif isinstance(error, commands.BadArgument):
            await ctx.message.reply(error_str("amount must be an integer"))
        else:
            await Jerubbaal.unhandled_error(ctx, error)

    @commands.command(alias=["undeafen", "ud"], usage="<member>", help="Move the player around 8 times")
    async def undeaf(self, ctx, member: discord.Member):
        if member.voice is None or member.voice.channel is None:
            await ctx.message.reply(error_str("target not in a channel"))
            return
        if ctx.author.voice is None or ctx.author.voice.channel is None or \
                ctx.author.voice.channel != member.voice.channel:

            await ctx.message.reply(error_str("you must be in the same channel with the target"))
            return
        if not member.voice.self_deaf:
            await ctx.message.reply(error_str("target is not deafened"))
            return

        orig_channel = member.voice.channel
        channels = ctx.guild.voice_channels[:len(ctx.guild.voice_channels) // 2]
        for channel in channels:
            if len(channel.members) != 0 or len(channel.voice_states) != 0 or channel == orig_channel or \
                    discord.Permissions.connect in channel.permissions_for(member):
                del channel

        for _ in range(8):
            if member.voice is not None and member.voice.channel is not None and member.voice.self_deaf:
                await member.edit(voice_channel=random.choice(channels))
            else:
                break
        if member.voice is not None and member.voice.channel is not None:
            await member.edit(voice_channel=orig_channel)
        await ctx.message.add_reaction("👍🏻")

    @undeaf.error
    async def undeaf_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("please specify member"))
        else:
            await Jerubbaal.unhandled_error(ctx, error)

    @commands.command(name="sendfile", aliases=["sf"], usage="<file>", help="Sends a file from a predetemined list")
    async def send_file(self, ctx, file):
        if file == "list":
            list_str = "Available file:\n"
            for sf_file in SEND_FILE_FILES.keys():
                list_str += f"\t- {sf_file}\n"
            await ctx.message.reply(list_str + "\n")
            return
        if file not in SEND_FILE_FILES.keys() or not os.path.isfile(SEND_FILE_FILES[file]):
            await ctx.message.reply(error_str("file doesn't exist"))
            return

        await ctx.send(file=discord.File(SEND_FILE_FILES[file]))
        await ctx.message.add_reaction("👍🏻")

    @send_file.error
    async def send_file_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing file!"))
        else:
            await Jerubbaal.unhandled_error(ctx, error)

    @commands.command(usage="<member>", help="Kicks a member, send them (privately) an invite link, and when they "
                                             "return their roles and nickname will be as of before the kick")
    async def kick(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.message.reply(error_str("you don't have permission!"))
            return
        if member.status != discord.Status.online:
            await ctx.message.reply(error_str("member must be online!"))
            return
        roles = member.roles
        nick = member.nick
        self.members_kicked[(member.id, ctx.guild.id)] = (nick, roles[1:])
        inv = await ctx.guild.text_channels[0].create_invite(max_uses=1)
        await member.send(content=f"Apparently, {ctx.author.name} kicked you. Come back through here: {inv.url}")
        await ctx.guild.kick(member)
        await ctx.message.add_reaction("👍🏻")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(error_str("missing target!"))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.reply(error_str("member not found"))
        else:
            await Jerubbaal.unhandled_error(ctx, error)

    @commands.command(usage="[length] <alias> <command>", help="Adds an alias to a command. Length defaults to 1. "
                                                               "To list the aliases, supply no arguments")
    async def alias(self, ctx, *args):
        if os.path.exists("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt"):
            with open("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt", "r") as f:
                self.aliases = json.loads(f.read())
        if len(args) == 0:
            msg = ""
            if len(self.aliases) == 0:
                msg += "\tThere are no aliases on this server!"
            else:
                msg = "Available aliases for this server:\n"
                for alias, value in self.aliases.items():
                    msg += f"\t- {alias}: {value}\n"
            await ctx.message.reply(msg)
            return
        len_alias = 1
        start = 0
        if args[0].isdigit():
            len_alias = int(args[start])
            start += 1
        if len(args) < start + len_alias + 2:
            await ctx.message.reply(error_str("your alias is not long enough"))
            return
        self.aliases[" ".join(args[start:start+len_alias])] = " ".join(args[start+len_alias:])
        with open("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt", "w") as f:
            f.write(json.dumps(self.aliases))
        await ctx.message.add_reaction("👍🏻")

    @commands.command(usage="<alias>", help="Delete an alias", name="deletealias", aliases=["delalias"])
    async def delalias(self, ctx, *args):
        if os.path.exists("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt"):
            with open("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt", "r") as f:
                self.aliases = json.loads(f.read())
        if " ".join(args) not in self.aliases.keys():
            await ctx.message.reply(error_str("alias doesn't exist"))
        self.aliases.pop(" ".join(args))
        with open("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt", "w") as f:
            f.write(json.dumps(self.aliases))
        await ctx.message.add_reaction("👍🏻")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            if os.path.exists("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt"):
                with open("..\\guilddata\\aliases_" + str(ctx.guild.id) + ".txt", "r") as f:
                    self.aliases = json.loads(f.read())
            args = ctx.message.content.split(" ")[1:]
            if " ".join(args) in self.aliases.keys():
                ctx.message.content = self.aliases[" ".join(args)]
                await self.bot.process_commands(ctx.message)
        else:
            # await Jerubbaal.unhandled_error(ctx, error)
            pass

    @commands.command(help="Shows this message")
    async def help(self, ctx):
        msg = "Available commands:\n"
        for cmd in sorted(jerubbaal_cog.get_commands(), key=lambda c: c.name):
            msg += f"\t**{cmd.name}"
            if len(cmd.aliases) != 0:
                msg += "(/" + "/".join(cmd.aliases) + ")"
            msg += "**"
            if cmd.usage is not None:
                msg += f" *{str(cmd.usage)}*"
            msg += f" - {str(cmd.help)}\n"
        await ctx.message.reply(msg)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if (member.id, member.guild.id) in self.members_kicked.keys():
            nick, roles = self.members_kicked[(member.id, member.guild.id)]
            await member.add_roles(*roles)
            await member.edit(nick=nick)
            self.members_kicked.pop((member.id, member.guild.id))

    @commands.Cog.listener()
    async def on_connect(self):
        global bot_owner
        print(f"Connected as {self.bot.user}")
        bot_owner = await bot.fetch_user(OWNER_ID)


token = ""
with open(r"..\tokens.txt", "r") as tokens:
    for line in tokens.readlines():
        splitted = line.split('=')
        if splitted[0] == TOKEN_NAME:
            token = splitted[1]
if token == "":
    print("File tokens.txt not found!")
    exit(1)

with open(r"..\owner_id.txt", "r") as ownerid:
    OWNER_ID = int(ownerid.read())
if OWNER_ID == 0:
    print("File owner_id.txt not found!")
    exit(1)

jerubbaal_cog = Jerubbaal(bot)
bot.add_cog(jerubbaal_cog)
bot.run(token)
