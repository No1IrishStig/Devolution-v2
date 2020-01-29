﻿import sys, traceback
import datetime
import discord
import asyncio
import random
import string
import json

import mysql.connector

from utils.functions import func
from utils.functions import sql
from discord.ext import commands
from utils.functions.func import lib
from utils.functions.checks import check

"""mydb = mysql.connector.connect(
    host="",
    user="root",
    passwd="",
    db="",
    port="3306"
)"""


config = func.get("./utils/config.json")

def randomString(stringLength=10):
    letters = "abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return "".join(random.choice(letters) for i in range(stringLength))

class Resurrection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(check.is_admin)
    async def fapply(self, ctx, user: discord.Member = None):
        channel = await self.bot.fetch_channel(638894822899580939)
        role = discord.utils.get(ctx.guild.roles, name="applied_tester")
        badrole = discord.utils.get(ctx.guild.roles, name="Tester")
        self.log(f"{ctx.author.id} Force Attempted {user.id} to apply for tester.")
        if not badrole in user.roles:
            if role in user.roles:
                err = await ctx.send(embed=lib.Editable_E("You have already applied to be a tester!", "", "Error"))
                await lib.erase(ctx, err)
            else:
                await user.add_roles(role)
                done = await ctx.send(embed=lib.Editable_S("You are now pending to become a tester!", "", "Resurrection"))
                await channel.send(embed=lib.Editable_S(f"{user.name} Applied for tester.", "", f"{user.id}"))
                await lib.erase(ctx, done)
        else:
            err2 = await ctx.send(embed=lib.Editable_E("You are already a tester!", "", "Resurrection"))
            await lib.erase(ctx, err2)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def apply(self, ctx):
        if str(ctx.guild.id) == "470607365733875732":
            channel = await self.bot.fetch_channel(638894822899580939)
            role = discord.utils.get(ctx.guild.roles, name="applied_tester")
            badrole = discord.utils.get(ctx.guild.roles, name="Tester")
            self.log(f"{ctx.author.id} Attempted to apply for tester.")
            if not badrole in ctx.author.roles:
                if role in ctx.author.roles:
                    err = await ctx.send(embed=lib.Editable_E("You have already applied to be a tester!", "", "Error"))
                    await lib.erase(ctx, err)
                else:
                    await ctx.author.add_roles(role)
                    done = await ctx.send(embed=lib.Editable_S("You are now pending to become a tester!", "", "Resurrection"))
                    await channel.send(embed=lib.Editable_S(f"{ctx.author.name} Applied for tester.", "", f"{ctx.author.id}"))
                    await lib.erase(ctx, done)
            else:
                err2 = await ctx.send(embed=lib.Editable_E("You are already a tester!", "", "Resurrection"))
                await lib.erase(ctx, err2)

    @commands.group(aliases=["res"], no_pm=True, invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def resurrection(self, ctx):
        if str(ctx.guild.id) == "470607365733875732":
            e = await ctx.send(embed=lib.Editable("Resurrection Commands", f"Use {ctx.prefix}resurrection help to view the commands\n\nCommands:\n{ctx.prefix}suggestion - Suggest a feature\n{ctx.prefix}issue - Report a bug\n{ctx.prefix}banr - Report an ingame ban**", "Resurrection"))
            await lib.erase(ctx, e)
        else:
            return

    @resurrection.group(no_pm=True, invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def help(self, ctx):
        if str(ctx.guild.id) == "470607365733875732":
            user = ctx.author
            await user.send(embed=lib.Editable("Resurrection Commands", f"Commands:\n**{ctx.prefix}suggestion (message)** - Submit a suggestion to the Development team \n**{ctx.prefix}issue (message)** - Submit a bug report to the Development team\n**{ctx.prefix}banr (message)** - Submit a ban report\n\n**!res help** - This page", "Resurrection"))
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            return

    @help.group(no_pm=True, invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def install(self, ctx):
        if str(ctx.guild.id) == "470607365733875732":
            user = ctx.author
            await user.send("https://resurrectionmenu.com/index.php?threads/ultimate-installation-guide.65/\n\nIf you still need help, use the #support channel!")
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            return

    @commands.command(no_pm=True, invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def issue(self, ctx, *args):
        if str(ctx.guild.id) == "470607365733875732":
            content = ""
            for word in args:
                content += word
                content += " "
            if content is "":
                e = await ctx.send(embed=lib.Editable("Oops!", f"To use that command properly, try this:\n\n**{ctx.prefix}issue (message)**", "Resurrection"))
                await lib.erase(ctx, e)
            else:
                channel = ctx.guild.get_channel(596781919216205873)
                bug = discord.Embed(
                colour=0xe8a848,
                description = content,
                timestamp=datetime.datetime.utcnow()
                )
                bug.set_author(name=f"Resurrection - Bug Report from {ctx.author.name}")
                bug.set_thumbnail(url="https://img.no1irishstig.co.uk/gkohk.png")
                await channel.send(embed=bug)
                await asyncio.sleep(5)
                await ctx.message.delete()
                self.log(f"{ctx.author.id} Submitted a bug report")
        else:
            return

    @commands.command(no_pm=True, invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def suggestion(self, ctx, *args):
        if str(ctx.guild.id) == "470607365733875732":
            content = ""
            for word in args:
                content += word
                content += " "
            if content is "":
                e = await ctx.send(embed=lib.Editable("Oops!", f"To use that command properly, try this:\n\n**{ctx.prefix}suggestion (message)**", "Resurrection"))
                await lib.erase(ctx, e)
            else:
                channel = ctx.guild.get_channel(596781919216205873)
                suggest = discord.Embed(
                colour=0x48cde8,
                description = content,
                timestamp=datetime.datetime.utcnow()
                )
                suggest.set_author(name=f"Resurrection - Suggestion from {ctx.author.name}")
                suggest.set_thumbnail(url="https://banner2.kisspng.com/20180616/czv/kisspng-cartoon-comics-clip-art-thinking-bulb-5b24f95e8df576.9573740515291497905815.jpg")
                suggestion = await channel.send(embed=suggest)
                await suggestion.add_reaction("👍")
                await suggestion.add_reaction("👎")
                await asyncio.sleep(5)
                await ctx.message.delete()
                self.log(f"{ctx.author.id} Submitted a suggestion")
        else:
            return

    @commands.command(no_pm=True, invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def banr(self, ctx, *args):
        if str(ctx.guild.id) == "470607365733875732":
            content = ""
            for word in args:
                content += word
                content += " "
            if content is "":
                e = await ctx.send(embed=lib.Editable("Oops!", f"To use that command properly, try this:\n\n**{ctx.prefix}banr (message)**", "Resurrection"))
                await lib.erase(ctx, e)
            else:
                channel = ctx.guild.get_channel(596781919216205873)
                ban = discord.Embed(
                colour=0xf54242,
                description = content,
                timestamp=datetime.datetime.utcnow()
                )
                ban.set_author(name=f"Resurrection - Ban Report from {ctx.author.name}")
                ban.set_thumbnail(url="https://img.no1irishstig.co.uk/6ucli.png")
                await channel.send(embed=ban)
                await asyncio.sleep(5)
                await ctx.message.delete()
                self.log(f"{ctx.author.id} Submitted a ban report")
        else:
            return

    """
    Key Gen -------------------------------------------------------------
    @commands.group(no_pm=True, invoke_without_command=True)
    async def key(self, ctx):
        if ctx.author.id in config.admins:
            e = await ctx.send(embed=lib.Editable("Key Gen Commands Commands", "Use `!key gen [auth, vip, upgrade] [amount]`", "Resurrection Key Gen"))
            await lib.erase(ctx, e)
        else:
            return

    @key.group(no_pm=True, invoke_without_command=True)
    async def gen(self, ctx):
        if ctx.author.id in config.admins:
            e = await ctx.send(embed=lib.Editable("Key Gen Commands", "Use `!key gen [auth, vip, upgrade] [amount]`", "Resurrection"))
            await lib.erase(ctx, e)
        else:
            return

    @gen.group(no_pm=True, invoke_without_command=True)
    async def auth(self, ctx, amount:int=None):
        if ctx.author.id in config.admins:
            authkeys = []
            if not amount is None:
                for f in range(amount):
                    mycursor = mydb.cursor()

                    sql = "INSERT INTO auth (gen, used_by, used_date) VALUES (%s, %s, %s)"
                    val = (randomString(16), None, None);
                    mycursor.execute(sql, val)
                    authkeys.append(str(val))
                    mydb.commit()

                await ctx.send(embed=lib.Editable(f"I generated {amount} Auth Keys!", "{}".format("\n").join(authkeys).replace('(', '').replace(')', '').replace("None", '').replace("'", '').replace(',', ''), "Auth Key Gen"))
            else:
                return
        else:
            return

    @gen.group(no_pm=True, invoke_without_command=True)
    async def vip(self, ctx, amount:int=None):
        if ctx.author.id in config.admins:
            vipkeys = []
            if not amount is None:
                for f in range(amount):
                    mycursor = mydb.cursor()

                    sql = "INSERT INTO premium (gen, used_by, used_date) VALUES (%s, %s, %s)"
                    val = (randomString(16), None, None);
                    mycursor.execute(sql, val)
                    vipkeys.append(str(val))
                    mydb.commit()

                await ctx.send(embed=lib.Editable(f"I generated {amount} VIP Keys!", "{}".format("\n").join(vipkeys).replace('(', '').replace(')', '').replace("None", '').replace("'", '').replace(',', ''), "VIP Key Gen"))
            else:
                return
        else:
            return

    @gen.group(no_pm=True, invoke_without_command=True)
    async def upgrade(self, ctx, amount:int=None):
        if ctx.author.id in config.admins:
            upgradekeys = []
            if not amount is None:
                for f in range(amount):
                    mycursor = mydb.cursor()

                    sql = "INSERT INTO upgrade (gen, used_by, used_date) VALUES (%s, %s, %s)"
                    val = (randomString(16), None, None);
                    mycursor.execute(sql, val)
                    upgradekeys.append(str(val))
                    mydb.commit()

                await ctx.send(embed=lib.Editable(f"I generated {amount} VIP Upgrade Keys!", "{}".format("\n").join(upgradekeys).replace('(', '').replace(')', '').replace("None", '').replace("'", '').replace(',', ''), "Upgrade Key Gen"))
            else:
                return
        else:
            return

    @key.group(no_pm=True, invoke_without_command=True)
    async def list(self, ctx):
        if ctx.author.id in config.admins:
            e = await ctx.send(embed=lib.Editable("Key Gen Commands", "Use `!key list [auth, vip, upgrade]`", "Resurrection"))
            await lib.erase(ctx, e)
        else:
            return

    @list.group(name="auth", no_pm=True, invoke_without_command=True)
    async def _auth(self, ctx):
        if ctx.author.id in config.admins:
            authlist = []
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM auth")
            myresult = mycursor.fetchall()

            count = 0
            for x in myresult:
              authlist.append(str(x))
              count = count + 1
            await ctx.send(embed=lib.Editable(f"I found {count} Authorized Keys!", "{}".format("\n").join(authlist).replace('(', '').replace(')', '').replace("None", '').replace("'", '').replace(',', ''), "Authorized Keys"))
        else:
            return

    @list.group(name="vip", no_pm=True, invoke_without_command=True)
    async def _vip(self, ctx, amount:int=None):
        if ctx.author.id in config.admins:
            viplist = []
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM vip")
            myresult = mycursor.fetchall()

            count = 0
            for x in myresult:
              viplist.append(str(x))
              count = count + 1
            await ctx.send(embed=lib.Editable_S(f"I found {count} VIP Keys!", "{}".format("\n").join(viplist).replace('(', '').replace(')', '').replace("None", '').replace("'", '').replace(',', ''), "VIP Keys"))
        else:
            return

    @list.group(name="upgrade", no_pm=True, invoke_without_command=True)
    async def _upgrade(self, ctx, amount:int=None):
        if ctx.author.id in config.admins:
            upgradelist = []
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM vipupgrade")
            myresult = mycursor.fetchall()

            count = 0
            for x in myresult:
              upgradelist.append(str(x))
              count = count + 1
            await ctx.send(embed=lib.Editable_S(f"I found {count} VIP Upgrade Keys!", "{}".format("\n").join(upgradelist).replace('(', '').replace(')', '').replace("None", '').replace("'", '').replace(',', ''), "Upgrade Keys"))
        else:
            return

    # ---------------------------------------------------------------------
    """

    @commands.command()
    async def create(self, ctx):
        if ctx.author.id in config.admins:
            general = discord.utils.get(ctx.guild.channels, name="general")
            await general.delete()

            await ctx.guild.edit(name="Resurrection Menu")

            # PERMISSIONS ------------------------------------------------------------------------------------------

            noperm = discord.Permissions()

            admin = discord.Permissions()
            admin.administrator = True

            stigrole = discord.Permissions()
            stigrole.administrator = True

            moderator = discord.utils.get(ctx.guild.roles, name="Moderator")

            mod = discord.Permissions()
            mod.view_audit_log = True
            mod.manage_guild = True
            mod.manage_roles = True
            mod.manage_channels = True
            mod.kick_members = True
            mod.ban_members = True
            mod.change_nickname = True
            mod.manage_nicknames = True
            mod.manage_emojis = True
            mod.send_messages = True
            mod.manage_messages = True
            mod.embed_links = True
            mod.attach_files = True
            mod.read_message_history = True
            mod.mention_everyone = True
            mod.external_emojis = True
            mod.add_reactions = True
            mod.connect = True
            mod.speak = True
            mod.mute_members = True
            mod.deafen_members = True
            mod.move_members = True
            mod.use_voice_activation = True

            # PERMISSIONS END -------------------------------------------------------------------------------------

            # ROLE CREATION ---------------------------------------------------------------------------------------
            await ctx.guild.create_role(name=".", permissions=admin)
            await ctx.guild.create_role(name="Admin", permissions=admin, colour=discord.Colour.dark_magenta())
            await ctx.guild.create_role(name="KEYGEN", permissions=noperm)
            await ctx.guild.create_role(name="HWID", permissions=noperm)
            await ctx.guild.create_role(name="Moderator", permissions=mod, colour=discord.Colour.magenta())
            await ctx.guild.create_role(name="Bot", permissions=noperm)
            await ctx.guild.create_role(name="Pre Order", permissions=noperm, colour=discord.Colour.gold())
            await ctx.guild.create_role(name="VIP", permissions=noperm, colour=discord.Colour.purple())
            await ctx.guild.create_role(name="Authorized", colour=discord.Colour.blue())
            await ctx.guild.create_role(name="Translator", permissions=noperm, colour=discord.Colour.orange())
            await ctx.guild.create_role(name="Reseller", permissions=noperm, colour=discord.Colour.orange())
            await ctx.guild.create_role(name="Tester", permissions=noperm, colour=discord.Colour.orange())
            await ctx.guild.create_role(name="Staff", permissions=noperm, colour=discord.Colour.dark_red())

            # ROLE CREATION END -----------------------------------------------------------------------------------

            # Categories & Channels -------------------------------------------------------------------------------

            Authorized = discord.utils.get(ctx.guild.roles, name="Authorized")
            Tester = discord.utils.get(ctx.guild.roles, name="Tester")
            Translator = discord.utils.get(ctx.guild.roles, name="Translator")
            Staff = discord.utils.get(ctx.guild.roles, name="Staff")
            Admin = discord.utils.get(ctx.guild.roles, name="Admin")

            print(Authorized)
            print(Tester)
            print(Translator)
            print(Staff)
            print(Admin)

            important_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True),
                Authorized: discord.PermissionOverwrite(read_messages=True, send_messages=False)
                }

            authorized_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True),
                Authorized: discord.PermissionOverwrite(read_messages=True)
                }

            voice_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True),
                Authorized: discord.PermissionOverwrite(read_messages=True)
                }

            tester_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True),
                Tester: discord.PermissionOverwrite(read_messages=True)
                }

            translator_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True),
                Translator: discord.PermissionOverwrite(read_messages=True)
                }

            staff_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True)
                }

            notifications_overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            Staff: discord.PermissionOverwrite(read_messages=True),
            Authorized: discord.PermissionOverwrite(read_messages=True, send_messages=False)
            }

            keys = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            Staff: discord.PermissionOverwrite(read_messages=False),
            Admin: discord.PermissionOverwrite(read_messages=True)
            }

            await ctx.guild.create_category(name="Important", overwrites=important_overwrites)
            await ctx.guild.create_category(name="Premium Channels", overwrites=authorized_overwrites)
            await ctx.guild.create_category(name="Voice Channels", overwrites=voice_overwrites)
            await ctx.guild.create_category(name="Tester Channels", overwrites=tester_overwrites)
            await ctx.guild.create_category(name="Translator Channels", overwrites=translator_overwrites)
            await ctx.guild.create_category(name="Staff", overwrites=staff_overwrites)

            category1 = discord.utils.get(ctx.guild.categories, name="Important")
            await category1.create_text_channel("welcome")
            await category1.create_text_channel("information")
            await category1.create_text_channel("rules")
            await category1.create_text_channel("faq")

            category2 = discord.utils.get(ctx.guild.categories, name="Premium Channels")
            await category2.create_text_channel("announcements")
            await category2.create_text_channel("general")
            await category2.create_text_channel("support")
            await category2.create_text_channel("notify")
            await category2.create_text_channel("notifications", overwrites=notifications_overwrites)
            await category2.create_text_channel("notification-comments")
            await category2.create_text_channel("commands")

            category3 = discord.utils.get(ctx.guild.categories, name="Voice Channels")
            await category3.create_voice_channel("General")
            await category3.create_voice_channel("Music")

            category4 = discord.utils.get(ctx.guild.categories, name="Tester Channels")
            await category4.create_text_channel("announcements")
            await category4.create_text_channel("testers")
            await category4.create_text_channel("bug-reports")

            category5 = discord.utils.get(ctx.guild.categories, name="Translator Channels")
            await category5.create_text_channel("translation-files")
            await category5.create_text_channel("translators")

            category6 = discord.utils.get(ctx.guild.categories, name="Staff")
            await category6.create_text_channel("staff-chat")
            await category6.create_text_channel("logs")
            await category6.create_text_channel("commands")
            await category6.create_text_channel("hwid")
            await category6.create_text_channel("keys", overwrites=keys)
            await category6.create_voice_channel("Voice")
            # Categories & Channels End --------------------------------------------------------------

            # Messages -------------------------------------------------------------------------------
            rules = discord.utils.get(ctx.guild.channels, name="rules")
            embed = discord.Embed(
                title="Rules",
                colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_author(name="Resurrection Menu", url="https://resurrectionmenu.com", icon_url="https://img.no1irishstig.co.uk/m9001.png")
            embed.set_footer()
            embed.add_field(name="**SOFTWARE**", value="You will be permanently banned without refund for...\n- Payment fraud\n- Account sharing\n- Malicious activity with the intent to undermine Resurrection Menu including but not limited to: dumping, reverse engineering", inline=False)
            embed.add_field(name="**FORUMS / DISCORD**", value="- In most cases, first time offenders will receive a warning. Second time offenders may receive a temporary ban. Third strike will result in a permanent ban.\n- No abusive/disrespectful behaviour towards any members of the server.\n- No selling or advertisement of accounts, keys, and/or any other gray/black market material.\n- No stupid usernames at all. You will be renamed without warning. This includes ASCII characters, invisible characters, and names solely to reach the top of the list.\n- No linking/posting or promoting of any other cheats or cheatprovider.\n- No spreading of personal information (e.g. doxxing)\n\nModerators may punish any user at their own discretion outside of this ruleset.", inline=False)
            await rules.send(embed=embed)

            information = discord.utils.get(ctx.guild.channels, name="information")
            await information.send("Set your name to your forum name and PM a Staff Member for your roles if you have purchased the menu!")

            faq = discord.utils.get(ctx.guild.channels, name="faq")
            embed = discord.Embed(
                title="FAQ",
                colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_author(name="Resurrection Menu", url="https://resurrectionmenu.com", icon_url="https://img.no1irishstig.co.uk/m9001.png")
            embed.set_footer()
            embed.add_field(name="ERROR -> Your HWID has been locked.", value="You need to message a moderator and give a valid reason due to why your computers hardware has appeared to change.", inline=False)
            embed.add_field(name="Why do I lose so much FPS?", value="The FPS drops will be improving in the upcoming builds, it is due to the encryption used on the files.", inline=False)
            embed.add_field(name="My menu won’t work help!**", value="Click [here](https://resurrectionmenu.com/index.php?threads/ultimate-installation-guide.65/) for installation help!", inline=False)
            embed.add_field(name="Why can’t I join heists / missions?", value="This is due to some remote protections, try turning some of them off (Kick Protection, Stat edit)", inline=False)
            embed.add_field(name="Why does my mechanic not work anymore?", value="Disable remote kick protection", inline=False)
            embed.add_field(name="Why do online options & all online options not work sometimes?", value="Players must be within 800 meters of you or else some of the options will not work on them.", inline=False)
            await faq.send(embed=embed)

            notify = discord.utils.get(ctx.guild.channels, name="notify")
            embed = discord.Embed(
                title="How to submit!",
                description="If you need help use !res help\n\nSpamming these commands will result in punishment.\n\nPlease dont send us duplicate suggestions and bug reports! Check in notifications first!",
                colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_author(name="Resurrection Menu", url="https://resurrectionmenu.com", icon_url="https://img.no1irishstig.co.uk/m9001.png")
            embed.set_footer()
            embed.add_field(name="Suggestions", value=f"{ctx.prefix}suggestion (suggestion)", inline=False)
            embed.add_field(name="Bug Reports", value=f"{ctx.prefix}issue (bug report)", inline=False)
            embed.add_field(name="Ban Reports", value=f"{ctx.prefix}issue (ban report)", inline=False)
            await notify.send(embed=embed)

            general = discord.utils.get(ctx.guild.channels, name="general")
            await general.send(embed=lib.Editable("Resurrection Recreated!", "The server has been made with all channels, roles and permissions as before.", "Server Generator"))

    def log(self, message):
        file = open("./utils/logs/Resurrection.log","a")
        file.write("[{}]: {} \n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (GMT)"), message))
        file.close()

def setup(bot):
    bot.add_cog(Resurrection(bot))
