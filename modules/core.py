import datetime
import discord
import asyncio
import aiohttp
import random
import time
import json

from discord import Spotify
from utils.functions import sql
from utils.functions import func
from discord.ext import commands
from utils.functions.func import lib
from random import choice as randchoice

config = func.get("utils/config.json")
insults = func.get("data/cmd_data/insults.json")

global page_number
page_number = None
global page_num
page_num = None
start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./data/settings/nsfw.json") as f:
            self.settings = json.load(f)

    @commands.Cog.listener(name="on_reaction_add")
    async def reaction_add_(self, reaction, user):
        global page_num
        emojis1 = ['◀', '▶', '🇽', '🇵']
        if not user.bot:
            if str(reaction.emoji in emojis1):

                if str(reaction.emoji) == '🇽':
                    try:
                        await help.delete()
                        page_num = None
                    except Exception as e:
                        return

                elif str(reaction.emoji) == '◀':
                    if page_num > 0:
                        await help.add_reaction("◀")
                        page_num -= 1
                        await reaction.remove(user)
                        if page_num == 0:
                            try:
                                await reaction.remove(self.bot.user)
                                await reaction.remove(user)
                            except Exception as e:
                                return
                    else:
                        try:
                            await reaction.remove(self.bot.user)
                            await reaction.remove(user)
                        except Exception as e:
                            return

                elif str(reaction.emoji) == '▶':
                    if page_num <= 5:
                        page_num += 1
                        await reaction.remove(user)
                        await help.add_reaction("◀")
                    else:
                        try:
                            await reaction.remove(self.bot.user)
                            await reaction.remove(user)
                        except Exception as e:
                            return

                elif str(reaction.emoji) == '🇵':
                    await user.send(embed=lib.Editable("Permission Requirements", "Manage Roles\nManage Channels\nKick Members\n Ban Members\nManage Nicknames\nRead Channels\nSend Messages\nManage Messages\nAdd Reactions\nConnect\nSpeak", "Help"))
                    await reaction.remove(user)

                if page_num == 0:
                    e = lib.Editable("Devolution - Help", "**Page 0** - This Page\n**Page 1** - Information\n**Page 2** - Fun\n**Page 3** - Useful\n**Page 4** - Moderation\n**Page 5** - Admin\n**Permission Help (P)** - DM's Required Permissions", "Help Index")
                    await help.edit(embed=e)

                elif page_num == 1:
                    e = lib.Editable(f"Devolution Help", "**help** - Gives help!\n**about** - Displays stuff about the bot\n**info** - Displays more bot information.\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**bug** - Use it to report bugs.\n**github** - Provides github link", "Information")
                    await help.edit(embed=e)

                elif page_num == 2:
                    e = lib.Editable(f"Devolution Help", "**bank** - Gives usage details\n**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour\n**roll** - Roles a dice\n**insult** - Insult people you dislike!\n**boobs** - See some melons!\n**ass** - See some peaches!\n**gif** - Search up a gif on giphy by name\n**gifr** - Gives a random gif from giphy\n**owo** - Get random responses", "Fun Help")
                    await help.edit(embed=e)

                elif page_num == 3:
                    e = lib.Editable("Devolution Help", "**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Sends a bot invite link\n**embed** - Creates an embed message\n**role** - Gives role options\n**math** - Gives usage details", "Useful Help")
                    await help.edit(embed=e)

                elif page_num == 4:
                    e = lib.Editable("Devolution Help", "**kick**- Kick a mentioned user\n**ban** - Ban a mentioned user\n**hackban** - Allows you to ban a UserID\n**punish** - Gives usage details\n**clean** - Cleans the current channel of bot messages and commands\n**cleanup** - Gives usage details\n**logs** - Gives usage details\n**warn** - Gives usage details\n**move** - Gives usage details", "Moderation Help")
                    await help.edit(embed=e)

                elif page_num == 5:
                    e = lib.Editable(f"Devolution Help", "**leave** - Makes the bot leave the guild\n**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**pm** - PMs Target user as bot\n**pmid** - PMs target ID as bot\n**amiadmin** - Tells you if you're a bot admin'", "Admin Help")
                    await help.edit(embed=e)

            else:
                return
        else:
            return

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        global page_num
        global help
        await ctx.message.delete()
        page_num = 0
        help = await ctx.send(embed = lib.Editable("Devolution - Help", "**Page 0** - This Page\n**Page 1** - Information\n**Page 2** - Fun\n**Page 3** - Useful\n**Page 4** - Moderation\n**Page 5** - Admin\n**Permission Help (P)** - DM's Required Permissions", "Help Index"))
        await help.add_reaction("🇽")
        await help.add_reaction("▶")
        await help.add_reaction("🇵")

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        user = ctx.author
        await ctx.message.add_reaction("📄")
        await user.send(f"Heres the link to invite me to your guilds!\n\nhttps://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8")
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(
            colour = 0xeb8034,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Uptime", value=text)
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Core")
        u = await ctx.send(embed=embed)
        await lib.erase(ctx, u)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx):
        embed=discord.Embed(
            title=f"About Devolution",
            description="Created with passion & for the greater good. Useful for guild Administration, Music, Fun and more.",
            colour = 0xeb8034
            )
        embed.set_author(name="Stig - Developer", icon_url="https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif?size=1024", url="https://github.com/No1IrishStig")
        embed.add_field(name="Discord Support", value="[Discord](https://discord.gg/V9DhKbW)", inline=True)
        embed.add_field(name="Programmed Using", value="[Python](https://www.python.org/) & [Discord.py](https://github.com/Rapptz/discord.py)", inline=True)
        embed.add_field(name="Version & API version", value=f"Build - {func.version}\n API Version - {discord.__version__}", inline=True)
        embed.set_footer(text="Devolution - Providing Discord since {}".format(self.bot.user.created_at.strftime("%d/%m/%Y")))
        await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def bug(self, ctx):
        f = await ctx.send(embed=lib.Editable("https://github.com/No1IrishStig/Devolution-v2/issues", "", "Bug Report"))
        await lib.erase(ctx, f)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        activeServers = self.bot.guilds
        sum = 0
        for s in activeServers:
            sum += len(s.members)
        embed=discord.Embed(
            title=f"Info about {self.bot.user.name}",
            description="Multifunctional Bot, constantly recieving updates.",
            colour = 0xeb8034
            )
        embed.set_author(name="Stig - Developer", icon_url="https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif?size=1024", url="https://github.com/No1IrishStig")
        embed.add_field(name="Discord Support", value="[Discord](https://discord.gg/V9DhKbW)", inline=True)
        embed.add_field(name="Source", value="[Github](https://github.com/No1IrishStig/Devolution-v2)", inline=True)
        embed.add_field(name="Currently Serving", value=f"{sum} Members in {len(self.bot.guilds)} Guild", inline=True)
        embed.set_footer(text="Devolution - Providing Discord since {}".format(self.bot.user.created_at.strftime("%d/%m/%Y")))
        await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sinfo(self, ctx):
        embed = discord.Embed(
            colour = 0xeb8034,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Creation Date", value=ctx.guild.created_at.strftime("%d/%m/%Y at %H:%M:%S"), inline=False)
        embed.add_field(name="Owner", value=ctx.guild.owner.name, inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Users", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="AFK Channel", value=ctx.guild.afk_channel, inline=True)
        embed.set_author(name=f"Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(icon_url=ctx.guild.icon_url, text=f"{ctx.guild.name} - {ctx.guild.id}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
            pass
        if user.voice is None:
            channel = "Not in a voice channel"
        else:
            channel = user.voice.channel.name
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    title = f"Listening to {activity.title} by {activity.artist}"
                else:
                    title = f"Playing {activity.name}"
        else:
            title = "Doing Nothing"
        embed = discord.Embed(
            title = title,
            colour = 0xeb8034,
            timestamp = datetime.datetime.utcnow()
            )
        embed.set_author(name = f"Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(text=f"{user.name}'s User Info", icon_url=user.avatar_url)
        embed.add_field(name="Joined At", value=user.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Role Count", value=len(user.roles), inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="Voice", value=channel, inline=True)
        await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user : discord.User=None):
        if user is None:
            user = ctx.author
            pass
        embed = discord.Embed(
            description = f"[Avatar]({user.avatar_url})",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=f"Devolution - Avatar Stealer", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        await ctx.send(embed=embed)

# Fun Commands --------------------------------------------------------------------------------

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command(no_pm=True, aliases=["cf"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx):
        await ctx.send("Flipping...")
        await asyncio.sleep(2)
        choices = ["Heads", "Tails"]
        rancoin = random.choice(choices)
        await ctx.send("You flipped a " + rancoin)

    @commands.command(aliases=["color"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def colour(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://www.colr.org/json/color/random") as r:
                res = await r.json(content_type=None)
                colour = res["new_color"]
                embedcolour = int(colour, 16)
                embed = discord.Embed(
                    title = "#" + colour,
                    colour = embedcolour
                    )
                await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def space(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://api.open-notify.org/iss-now.json") as r:
                res = await r.json()
                async with cs.get("http://api.open-notify.org/astros.json") as r2:
                    res2 = await r2.json()
                    latitude = res["iss_position"]["latitude"]
                    longitude = res["iss_position"]["longitude"]
                    people = res2["number"]
                    name = ctx.author.name
                    avatar = ctx.author.avatar_url
                    embed = discord.Embed(
                        title = "International Space Station",
                        colour = 0xeb8034,
                        timestamp=datetime.datetime.utcnow()
                        )
                    embed.add_field(name="Longitude", value=f"{longitude}", inline=True)
                    embed.add_field(name="Latitude", value=f"{latitude}", inline=True)
                    embed.add_field(name="People in Space", value=f"{people}", inline=True)
                    embed.set_footer(text="Devolution - Space", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                    await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roll(self, ctx, number : int = 100):
        author = ctx.author
        if number > 1:
            n = random.randint(1, number)
            await ctx.send(f"{author.mention} :game_die: {n} :game_die:")
        else:
            number = 69
            n = random.randint(1, number)
            await ctx.send(f"{author.mention} :game_die: {n} :game_die:")

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def insult(self, ctx, user : discord.Member=None):
        author = ctx.author
        msg = " "
        if user != None:
            if user.id == self.bot.user.id:
                msg = "How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
                await ctx.send(author.mention + msg)
            else:
                await ctx.send(user.mention + msg + randchoice(insults))
        else:
            await ctx.send(author.mention + msg + randchoice(insults))

    @commands.command(no_pm=True, aliases=["tits"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def boobs(self, ctx):
        author = ctx.author
        rdm = random.randint(0, self.settings["ama_boobs"])
        search = (f"http://api.oboobs.ru/boobs/{rdm}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json()
                boob = randchoice(result)
                boob = "http://media.oboobs.ru/{}".format(boob["preview"])
            embed = discord.Embed(
                colour = 0xff8cee,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_image(url=boob)
            embed.set_footer(text=f"Devolution - Tits", icon_url="https://i.imgur.com/BS6YRcT.jpg")
            e = await ctx.send(embed=embed)

    @commands.command(no_pm=True, aliases=["booty"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ass(self, ctx):
        author = ctx.author
        rdm = random.randint(0, self.settings["ama_ass"])
        search = (f"http://api.obutts.ru/butts/{rdm}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json(content_type=None)
                ass = randchoice(result)
                ass = "http://media.obutts.ru/{}".format(ass["preview"])
            embed = discord.Embed(
                colour = 0xff8cee,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_image(url=ass)
            embed.set_footer(text=f"Devolution - Ass", icon_url="https://i.imgur.com/BS6YRcT.jpg")
            e = await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gif(self, ctx, *keywords):
        url = (f"http://api.giphy.com/v1/gifs/search?&api_key=dc6zaTOxFJmzC&q={keywords}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        g = result["data"][0]["url"]
                        await ctx.send(g)
                    else:
                        e = await ctx.send(embed=lib.Editable_E("No search results found", "", "Error"))
                        await lib.erase(ctx, e)
                else:
                    ee = await ctx.send(embed=lib.Editable_E("Error Contacting API", "", "Error"))
                    await lib.erase(ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gifr(self, ctx, *keywords):
        url = (f"http://api.giphy.com/v1/gifs/random?&api_key=dc6zaTOxFJmzC&tag={keywords}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        g = result["data"]["url"]
                        await ctx.send(g)
                    else:
                        e = await ctx.send(embed=lib.Editable_E("No search results found", "", "Error"))
                        await lib.erase(ctx, e)
                else:
                    ee = await ctx.send(embed=lib.Editable_E("Error Contacting API", "", "Error"))
                    await lib.erase(ctx, ee)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def math(self, ctx, num1 : int=0, op=None, num2 : int=0):
        if num1 and op and num2:
            if op == "+":
                ans = num1 + num2
            elif op == "-":
                ans = num1 - num2
            elif op == "*":
                ans = num1 * num2
            elif op == "/":
                ans = num1 / num2
            await ctx.send(embed=lib.Editable(f"You requested {num1} {op} {num2}", f"{num1} {op} {num2} = {ans}", "Maths"))
        else:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments", "Usage Examples:\n\n1 + 1\n1 - 1\n 1 * 1\n 1 / 1", "Error"))

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def amiadmin(self, ctx):
        if ctx.author.id in config.admins:
            await ctx.send(f"Yes {ctx.author.mention}, you're an admin!")
        else:
            await ctx.send(f"You arent an admin, {ctx.author.mention}")

# Leveling System Start ------------------------------------------------------------------

    """@commands.Cog.listener(name="on_message")
    async def on_message_(self, message):
        try:
            GID = str(message.guild.id)
            UID = str(message.author.id)
            if GID in self.levels:
                if self.levels[GID]["Enabled"] is True:
                    if message.author != self.bot.user:
                        if self.db_exists(GID, UID):
                            if self.user_exists(GID, UID):
                                self.add_xp(GID, UID)
                                await self.level_up(message)
                                self.db.sync()
                            else:
                                self.setup(message)
                        else:
                            self.setup(message)
                    else:
                        return
                else:
                    return
            else:
                self.levels[GID] = {"Enabled": True, "Messages": True}
                with open("./data/settings/leveling.json", "w") as f:
                    json.dump(self.levels, f)
        except AttributeError:
            return

    @commands.group(invoke_without_command=True)
    async def leveling(self, ctx):
        await ctx.send(embed=lib.Editable("Information", f"`{ctx.prefix}leveling progress` - Shows your progress to the next level\n`{ctx.prefix}leveling calculate (level)` - Gives you the required XP for given level\n\n**Admin Commands**\n`{ctx.prefix}leaderboard` - To show the highest rankers in the server\n`{ctx.prefix}leveling toggle` - To enable the leveling system\n`{ctx.prefix}leveling toggle messages` - Disables level up messages for the guild", "Leveling"))

    @leveling.group(invoke_without_command=True)
    async def progress(self, ctx):
        global required_xp
        GID = str(ctx.guild.id)
        UID = str(ctx.author.id)
        xp = self.db["Levels"][GID][UID]["xp"]
        level = self.db["Levels"][GID][UID]["level"]
        await ctx.send(embed=lib.Editable(f"{ctx.author.name}'s Level Progression Report", f"Your XP: {xp}\nYour Level: {level}\n\nLevel {level + 1} requires: {required_xp} XP\n XP To Level Up: {required_xp - xp} XP", "Leveling"))

    @leveling.group(invoke_without_command=True)
    async def calculate(self, ctx, level :int = None):
        if level:
            xp = level * 25
            await ctx.send(embed=lib.Editable(f"Level {level} Calculation", f"Level {level} requires {xp} XP", "Leveling"))

    @leveling.group(invoke_without_command=True)
    async def toggle(self, ctx):
        GID = str(ctx.guild.id)
        if ctx.author.guild_permissions.manage_roles:
            if GID in self.levels:
                if self.levels[GID]["Enabled"] is False:
                    self.levels[GID]["Enabled"] = True
                    await ctx.send(embed=lib.Editable("Leveling System is now Enabled", f"The leveling system has been enabled for {ctx.guild.name}", "Leveling"))
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)
                else:
                    self.levels[GID]["Enabled"] = False
                    await ctx.send(embed=lib.Editable("Leveling System is now Disabled", f"The leveling system has been disabled for {ctx.guild.name}", "Leveling"))
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)
            else:
                self.levels[GID] = {"Enabled": True, "Messages": True}
                await ctx.send(embed=lib.Editable("Leveling", "Leveling is enabled with messages.", "Leveling"))
                with open("./data/settings/leveling.json", "w") as f:
                    json.dump(self.levels, f)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, p)

    @commands.command()
    async def leaderboard(self, ctx):
        GID = str(ctx.guild.id)
        UID = str(ctx.author.id)
        if self.user_exists:
            top = 10
            level_sorted = sorted(self.db["Levels"][GID].items(), key=lambda x: x[1]["xp"], reverse=True)
            if len(level_sorted) < top:
                top = len(level_sorted)
            topten = level_sorted[:top]
            highscore = ""
            place = 1
            for id in topten:
                highscore += str(place).ljust(len(str(top))+1)
                highscore += (id[1]["name"]+ "'s XP:" + " ").ljust(23-len(str(id[1]["xp"])))
                highscore += str(id[1]["xp"]) + "\n"
                place += 1
            await ctx.send(embed=lib.Editable(f"Top 10", f"{highscore}", "Leveling"))
        else:
            self.setup(message)

    @toggle.group()
    async def messages(self, ctx):
        GID = str(ctx.guild.id)
        if ctx.author.guild_permissions.manage_roles:
            if GID in self.levels:
                if self.levels[GID]["Messages"] is False:
                    self.levels[GID]["Messages"] = True
                    await ctx.send(embed=lib.Editable("Leveling Announcements are now Enabled", f"The leveling announcements have been enabled for {ctx.guild.name}", "Leveling"))
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)
                else:
                    self.levels[GID]["Messages"] = False
                    await ctx.send(embed=lib.Editable("Leveling Announcements are now Disabled", f"The leveling announcements have been disabled for {ctx.guild.name}", "Leveling"))
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)

            else:
                self.levels[GID] = {"Enabled": True, "Messages": True}
                await ctx.reinvoke()
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, p)

    def db_exists(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if GID in self.db["Levels"]:
            return True
        else:
            return False

    def user_exists(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if self.db_exists:
            if UID in self.db["Levels"][GID]:
                return True
            else:
                return False
        else:
            return False

    def add_xp(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if self.user_exists(GID, UID):
            self.db["Levels"][GID][UID]["xp"] += 1

    def setup(self, message):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        user = message.author
        if self.db_exists(GID, UID):
            if not self.user_exists(GID, UID):
                self.db["Levels"][GID] = {UID: {"name": user.name, "level": 0, "xp": 0}}
                self.db.sync()
        else:
            self.db["Levels"][GID] = {UID: {"name": user.name, "level": 0, "xp": 0}}
            self.db.sync()

    async def level_up(self, message):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        global required_xp
        if self.user_exists:
            xp = self.db["Levels"][GID][UID]["xp"]
            level = self.db["Levels"][GID][UID]["level"]
            if level == 0:
                required_xp = 15
                pass
            else:
                required_xp = 25 * level
                # print(f"XP: {xp}\nLevel: {level}\nRequired XP: {required_xp}")
                pass
            if xp >= required_xp:
                self.db["Levels"][GID][UID]["level"] += 1
                if self.levels[GID]["Messages"] is True:
                    await message.channel.send(embed=lib.Editable("Level Up!", f"{message.author.name} Leveled up to {level + 1}", "Leveling"))
        else:
            await self.setup(message)"""


def setup(bot):
    bot.add_cog(Core(bot))
