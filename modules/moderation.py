import datetime
import asyncio
import discord
import json
import os

from utils.functions import func
from utils.functions import sql
from discord.ext import commands
from utils.functions.func import lib
from utils.functions.checks import check

config = func.get("utils/config.json")
punished_users = []
log_settings = {"embed": False, "Channel": None, "edit": False, "delete": False, "user": False, "join": False, "leave": False, "server": False}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./data/settings/logs.json") as f:
            self.logs = json.load(f)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def say(self, ctx, *args):
        message = ' '.join(args)
        if not message == "":
            await ctx.send(message)
        else:
            await ctx.send(embed=lib.Editable_E("Give me something to say", "", "Error"))

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, user: discord.User=None, *args):
        if ctx.author.guild_permissions.kick_members or ctx.author.id in config.admins:
            if user:
                reason = ' '.join(args)
                if reason == "":
                    await user.send(embed=lib.Editable("You were kicked", f"You were kicked from '{ctx.guild.name}' by {ctx.author}", "Moderation"), delete_after=config.deltimer)
                    await ctx.send(embed=lib.Editable_S("Success", f"User has been kicked by {ctx.author.name}", "Moderation"), delete_after=config.deltimer)
                    await ctx.guild.kick(user)
                else:
                    await user.send(embed=lib.Editable("You were kicked", f"You were kicked from '{ctx.guild.name}' by {ctx.author} for '{reason}'", "Moderation"), delete_after=config.deltimer)
                    await ctx.send(embed=lib.Editable_S("Success", f"User has been kicked by {ctx.author.name} for '{reason}'", "Moderation"), delete_after=config.deltimer)
                    await ctx.guild.kick(user)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}kick @someone @reason\n\nOptional Arguments:\nReason", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, user: discord.User=None, *args):
        if ctx.author.guild_permissions.ban_members or ctx.author.id in config.admins:
            if user:
                reason = ' '.join(args)
                if reason == "":
                    await user.send(embed=lib.Editable("You were banned", f"You were banned from '{ctx.guild.name}' by {ctx.author}", "Moderation"), delete_after=config.deltimer)
                    await ctx.send(embed=lib.Editable_S("Success", f"User has been banned by {ctx.author.name}", "Moderation"), delete_after=config.deltimer)
                    await ctx.guild.ban(user)
                else:
                    await user.send(embed=lib.Editable("You were banned", f"You were banned from '{ctx.guild.name}' by {ctx.author} for '{reason}'", "Moderation"), delete_after=config.deltimer)
                    await ctx.send(embed=lib.Editable_S("Success", f"User has been banned by {ctx.author.name} for '{reason}'", "Moderation"), delete_after=config.deltimer)
                    await ctx.guild.ban(user)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}ban @someone @reason\n\nOptional Arguments:\nReason", "Usage"), delete_after=config.deltimer)

        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hackban(self, ctx, user_id: int=None, *args):
        if ctx.author.guild_permissions.ban_members or ctx.author.id in config.admins:
            if user_id:
                reason = ' '.join(args)
                if reason == "":
                    user = await self.bot.fetch_user(user_id)
                    y = await ctx.send(embed=lib.Editable_S(f"{ctx.author.name} Just yeeted someone!", f"UserID '{user_id}' just got hackbanned!", "Moderation"), delete_after=config.deltimer)
                    await user.send(embed=lib.Editable("You got hackbanned!", f"You got hack banned from '{ctx.guild.name}'", "Moderation"), delete_after=config.deltimer)
                    await ctx.guild.ban(user)
                else:
                    user = await self.bot.fetch_user(user_id)
                    y1 = await ctx.send(embed=lib.Editable_S(f"{ctx.author.name} Just yeeted someone!", f"UserID '{user_id}' just got hackbanned for {reason}!", "Moderation"), delete_after=config.deltimer)
                    await user.send(embed=lib.Editable("You got hackbanned!", f"You got hack banned from '{ctx.guild.name}' for '{reason}'", "Moderation"), delete_after=config.deltimer)
                    await ctx.guild.ban(user)
            else:
                e = await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}hackban @someone @reason\n\nOptional Arguments:\nReason", "Usage"), delete_after=config.deltimer)
        else:
            p = await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def punish(self, ctx, member: discord.Member=None, time:int=None):
        if member:
            role = discord.utils.get(member.guild.roles, name="punished")
            if member.top_role < ctx.author.top_role:
                if role in ctx.guild.roles:
                    if not role in member.roles:
                        punished_users.append(member.id)
                        if time:
                            await member.send(embed=lib.Editable("Punished!", f"You were punished from '{ctx.guild.name}' by {ctx.author.name} for {time} seconds", "Moderation"), delete_after=config.deltimer)
                            s1 = await ctx.send(embed=lib.Editable_S(f"{member.name} Punished", f"{ctx.author.mention} punished {member.mention} for {time} seconds.", "Moderation"), delete_after=config.deltimer)
                            await member.add_roles(role)
                            await asyncio.sleep(time)
                            await member.remove_roles(role)
                            if member.id in punished_users:
                                await member.send(embed=lib.Editable("Punished!", f"Your punishment in '{ctx.guild.name}' has expired", "Moderation"), delete_after=config.deltimer)
                        else:
                            await member.send(embed=lib.Editable("Punished!", f"You were punished from '{ctx.guild.name}' by {ctx.author.name}", "Moderation"), delete_after=config.deltimer)
                            await ctx.send(embed=lib.Editable_S(f"{member.name} Unpunished", f"{ctx.author.name} punished {member.mention}", "Moderation"), delete_after=config.deltimer)
                            await member.add_roles(role)
                    else:
                        await ctx.send(embed=lib.Editable_E("User is already punished", "", "Error"), delete_after=config.deltimer)
                else:
                    await self.punish_create(ctx)
            else:
                await ctx.send(embed=lib.Editable_E("You cannot punish that user.", "", "Error"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}punish @someone (time)\n\nOptional Arguments: Time (Seconds)", "Usage"), delete_after=config.deltimer)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unpunish(self, ctx, member: discord.Member=None):
        if member:
            role = discord.utils.get(member.guild.roles, name="punished")
            if role in ctx.guild.roles:
                if role in member.roles:
                    await member.send(embed=lib.Editable("Unpunished!", f"You were unpunished from '{ctx.guild.name}' by {ctx.author.name}", "Moderation"))
                    await ctx.send(embed=lib.Editable_S(f"{member.name} Unpunished", f"{ctx.author.name} unpunished {member.mention}", "Moderation"), delete_after=config.deltimer)
                    await member.remove_roles(role)
                    punished_users.remove(member.id)
                else:
                    await ctx.send(embed=lib.Editable_E("User is not punished", "", "Error"), delete_after=config.deltimer)
            else:
                await self.punish_create(ctx)
        else:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}unpunish @someone", "Usage"), delete_after=config.deltimer)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def lspunish(self, ctx):
        users = []
        for id in punished_users:
            user = await self.bot.fetch_user(id)
            users.append(user.name)
        await ctx.send(embed=lib.Editable("Punished List", "{}".format("\n ".join(users)), "Moderation"), delete_after=30)

    @commands.command()
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def spp(self, ctx):
        await self.punish_create(ctx)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def embed(self, ctx):
        await ctx.message.delete()
        question = await ctx.send(embed=lib.Editable("Embed Generator", "Please type your title!", "Embed Generation"))
        title = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
        await title.delete()
        e = lib.Editable(title.content, "Please type your footer!", "Embed Generation")
        await question.edit(embed=e)
        footer = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
        await footer.delete()
        e = lib.Editable(title.content, "Please type your description!", footer.content)
        await question.edit(embed=e)
        description = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
        await description.delete()
        e = lib.Editable(title.content, description.content, footer.content)
        await question.edit(embed=e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rename(self, ctx, member:discord.Member=None, *args):
        if ctx.author.guild_permissions.manage_nicknames:
            name = ' '.join(args)
            if member and not name is "":
                await member.edit(nick=name)
                await ctx.send(embed=lib.Editable_S(f"{member.name} was renamed to '{member.name}'", "", "Moderation"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}rename @someone (nickname)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @commands.command(no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clean(self, ctx):
        number = 99
        prefixes = [config.prefix]

        if "" in prefixes:
            prefixes.pop("")

        def check(m):
            if ctx.author.id == self.bot.user.id:
                return True
            elif m == ctx.message:
                return True
            p = discord.utils.find(m.content.startswith, prefixes)
            if p and len(p) > 0:
                return m.content[len(p):]
            return False

        to_delete = [ctx.message]

        tries_left = 5
        tmp = ctx.message

        while tries_left and len(to_delete) - 1 < number:
            async for message in ctx.channel.history(limit=number, before=tmp):
                if len(to_delete) - 1 < number and check(message):
                    to_delete.append(message)
                tmp = message
            tries_left -= 1

            await ctx.channel.delete_messages(to_delete)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cleanup(self, ctx):
        await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"{ctx.prefix}cleanup after\n{ctx.prefix}cleanup messages\n{ctx.prefix}cleanup user", "Usage"), delete_after=config.deltimer)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def after(self, ctx, id=None):
        if id:
            to_delete = []
            after = await ctx.channel.fetch_message(id)
            async for message in ctx.channel.history(limit=100, after=after):
                to_delete.append(message)
            await ctx.channel.delete_messages(to_delete)
        else:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}cleanup after (ID)", "Usage"), delete_after=config.deltimer)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def messages(self, ctx, num:int=None):
        if ctx.author.guild_permissions.manage_messages:
            if num is None:
                await ctx.send(embed=lib.Editable("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}cleanup messages (amount)", "Usage"), delete_after=config.deltimer)
            else:
                await ctx.channel.purge(limit=num + 1)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)


    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def user(self, ctx, user: discord.Member=None, number: int=None):
        if user and number:
            def check(m):
                if ctx.author == user:
                    return True
                elif m == ctx.message:
                    return True
                else:
                    return False

            to_delete = [ctx.message]
            tries_left = 5
            tmp = ctx.message

            while tries_left and len(to_delete) - 1 < number:
                async for message in ctx.channel.history(limit=number, before=tmp):
                    if len(to_delete) - 1 < number and check(message):
                        to_delete.append(message)
                    tmp = message
                tries_left -= 1
                await ctx.channel.delete_messages(to_delete)
        else:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}cleanup user (@user) (amount)", "Usage"), delete_after=config.deltimer)

    @commands.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    async def move(self, ctx):
        await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"{ctx.prefix}move count\n{ctx.prefix}move all\n{ctx.prefix}move role\n{ctx.prefix}move channel #voicechannel", "Usage"), delete_after=config.deltimer)

    @move.group()
    @commands.check(check.is_moderator)
    async def count(self, ctx):
        if ctx.author.voice.channel:
            list_of_channels = ctx.guild.voice_channels
            for voice_channels in list_of_channels:
                if len(voice_channels.members) > 0:
                    await ctx.send(embed=lib.Editable_S(f"Found {len(voice_channels.members)} Member(s) in '{voice_channels.name}'", "", "Voice Moderation"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Join a voice channel", f"", "Error"), delete_after=config.deltimer)

    @move.group()
    @commands.check(check.is_moderator)
    async def all(self, ctx):
        list_of_channels = ctx.guild.voice_channels
        userlist = []
        membercount = 0
        channel_count = 0
        move_to = ctx.author.voice.channel
        if ctx.author.voice.channel:
            for voice_channels in list_of_channels:
                if len(voice_channels.members) > 0:
                    membercount += len(voice_channels.members)
                    channel_count += 1
                for members in voice_channels.members:
                    if members.bot is False:
                        await members.move_to(ctx.author.voice.channel)
                        userlist.append(members.name)
                    else:
                        membercount -= 1
            await ctx.send(embed=lib.Editable("Fetching Users...", "Found {} Users in {} Voice Channels. Moved them to '{}' under the command of {}".format(membercount, channel_count, move_to, ctx.author.name), "Voice Moderation"), delete_after=config.deltimer)
            membercount = 0
        else:
            await ctx.send(embed=lib.Editable_E("Join a voice channel", f"", "Error"), delete_after=config.deltimer)

    @move.group(name="role")
    @commands.check(check.is_moderator)
    async def role_(self, ctx, rolename:str=None):
        if ctx.author.voice.channel:
            move_to = ctx.author.voice.channel
            list_of_channels = ctx.guild.voice_channels
            membercount = 0
            if rolename:
                role = discord.utils.get(ctx.guild.roles, name=rolename)
                for voice_channels in list_of_channels:
                    if len(voice_channels.members) > 0:
                        for members in voice_channels.members:
                            if members.bot is False:
                                if role in members.roles:
                                    membercount += 1
                                    await members.move_to(move_to)
                await ctx.send(embed=lib.Editable("Fetching Users...", "Found {} Users with the role '{}'. Moved them to '{}' under the command of {}".format(membercount, rolename, move_to, ctx.author.name), "Voice Moderation"), delete_after=config.deltimer)
                membercount = 0
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Role", "", "Error"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Join a voice channel", f"", "Error"), delete_after=config.deltimer)

    @move.group(name="channel")
    @commands.check(check.is_moderator)
    async def channel_(self, ctx, channelname: str=None):
        if ctx.author.voice.channel:
            move_to = ctx.author.voice.channel
            list_of_channels = ctx.guild.voice_channels
            membercount = 0
            if channelname:
                for channels in ctx.guild.voice_channels:
                    if channels.name == channelname:
                        for members in channels.members:
                            if members.bot is False:
                                membercount += len(channels.members)
                                await members.move_to(move_to)
                await ctx.send(embed=lib.Editable("Fetching Users...", "Found **{}** Users in channel **{}**. Moved them to {} under the command of **{}**".format(membercount, channelname, move_to, ctx.author.name), "Voice Moderation"), delete_after=config.deltimer)
                membercount = 0
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Channel", f"Usage Example:\n\n{ctx.prefix}move channel (channelname)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Join a voice channel", f"", "Error"), delete_after=config.deltimer)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def role(self, ctx):
        if ctx.author.guild_permissions.manage_roles or ctx.author.id in config.admins:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"{ctx.prefix}role add\n{ctx.prefix}role list\n{ctx.prefix}role remove\n{ctx.prefix}role create", "Usage"), delete_after=config.deltimer)

        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @role.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def list(self, ctx):
        if ctx.author.guild_permissions.manage_roles or ctx.author.id in config.admins:
            roles = []
            for role in ctx.guild.roles:
                roles.append(role.name)
            roles.remove("@everyone")
            await ctx.send(embed=lib.Editable("Role List", "{}".format("\n".join(roles)), "Roles"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @role.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def add(self, ctx, member: discord.Member=None, rolename=None ):
        if ctx.author.guild_permissions.manage_roles or ctx.author.id in config.admins:
            if member and rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if not role in member.roles:
                        await member.add_roles(role)
                        await ctx.send(embed=lib.Editable_S("Role Added", f"The role '{role}' was added to {member.mention}", "Roles"), delete_after=config.deltimer)
                    else:
                        await ctx.send(embed=lib.Editable_E(f"{member.name} already has that role", "", "Error"), delete_after=config.deltimer)
                else:
                    await ctx.send(embed=lib.Editable_E("Invalid Role", "", "Error"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}role add @someone (role)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)


    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove(self, ctx, member: discord.Member=None, rolename=None):
        if ctx.author.guild_permissions.manage_roles or ctx.author.id in config.admins:
            if member and rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if role in member.roles:
                        await member.remove_roles(role)
                        await ctx.send(embed=lib.Editable_S("Role Removed", f"The role '{role}' was removed from {member.name}", "Roles"), delete_after=config.deltimer)
                    else:
                        await ctx.send(embed=lib.Editable_E(f"{member.name} does not have that role", "", "Error"), delete_after=config.deltimer)
                else:
                    await ctx.send(embed=lib.Editable_E("Invalid Role", "", "Error"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}role remove @someone (role)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles or ctx.author.id in config.admins:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if not role in ctx.message.guild.roles:
                    await ctx.guild.create_role(name=rolename)
                    await ctx.send(embed=lib.Editable_S("Role Created", f"The role '{rolename}' has been created.", "Roles"), delete_after=config.deltimer)
                else:
                    await ctx.send(embed=lib.Editable_E("That role already exists", "", "Error"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}role create (role)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles or ctx.author.id in config.admins:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    await role.delete()
                    await ctx.send(embed=lib.Editable_S(f"Role {rolename} was deleted", "", "Roles"), delete_after=config.deltimer)
                else:
                    await ctx.send(embed=lib.Editable_E("That role doesnt exist", "", "Error"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}role delete (role)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.NoPerm(), delete_after=config.deltimer)

# Logs Start -------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def logs(self, ctx):
        GID = str(ctx.guild.id)
        await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"{ctx.prefix}logs set channel\n{ctx.prefix}logs toggle\n{ctx.prefix}logs toggle all", "Logs"), delete_after=config.deltimer)

    @logs.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set(self, ctx):
        await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"{ctx.prefix}logs set channel\n{ctx.prefix}logs toggle\n{ctx.prefix}logs toggle all", "Logs"), delete_after=config.deltimer)

    @set.group(name="channel", invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set_channel(self, ctx):
        GID = str(ctx.guild.id)
        if GID in self.logs:
            self.logs[GID]["Channel"] = ctx.channel.id
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S(f"Channel set to {ctx.channel.name}", "", "Logs"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Please enable The logs first", f"{ctx.prefix}logs enable", "Error"), delete_after=config.deltimer)

    @logs.group(invoke_without_command=True, no_pm=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def toggle(self, ctx):
        GID = str(ctx.guild.id)
        e = discord.Embed(title = f"Logs Settings for {ctx.guild.name}", colour = 0x9bf442)
        e.add_field(name="Delete", value=str(self.logs[GID]['delete']))
        e.add_field(name="Edit", value=str(self.logs[GID]['edit']))
        e.add_field(name="User", value=str(self.logs[GID]['user']))
        e.add_field(name="Join", value=str(self.logs[GID]['join']))
        e.add_field(name="Leave", value=str(self.logs[GID]['leave']))
        e.add_field(name="Server", value=str(self.logs[GID]['server']))
        e.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=e)

    @logs.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def enable(self, ctx):
            GID = str(ctx.guild.id)
            if not GID in self.logs:
                self.logs[GID] = log_settings
                self.logs[GID]["Channel"] = ctx.channel.id
                with open("./data/settings/logs.json", "w") as f:
                    json.dump(self.logs, f)
                    await ctx.send(embed=lib.Editable_S("Logs are now enabled", "", "Logs"), delete_after=config.deltimer)
            else:
                del self.logs[GID]
                with open("./data/settings/logs.json", "w") as f:
                    json.dump(self.logs, f)
                    await ctx.send(embed=lib.Editable_S("Logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx):
        GID = str(ctx.guild.id)
        if self.logs[GID]["delete"] == False:
            self.logs[GID]["delete"] = True
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S("Delete logs are now enabled", "", "Logs"), delete_after=config.deltimer)
        elif self.logs[GID]["delete"] == True:
            self.logs[GID]["delete"] = False
            with open("./data/settings/logs.json", "w") as e:
                json.dump(self.logs, e)
                await ctx.send(embed=lib.Editable_S("Delete logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def edit(self, ctx):
        GID = str(ctx.guild.id)
        if self.logs[GID]["edit"] == False:
            self.logs[GID]["edit"] = True
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S("Edit logs are now enabled", "", "Logs"), delete_after=config.deltimer)
        elif self.logs[GID]["edit"] == True:
            self.logs[GID]["edit"] = False
            with open("./data/settings/logs.json", "w") as e:
                json.dump(self.logs, e)
                await ctx.send(embed=lib.Editable_S("Edit logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def user(self, ctx):
        GID = str(ctx.guild.id)
        if self.logs[GID]["user"] == False:
            self.logs[GID]["user"] = True
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S("User logs are now enabled", "", "Logs"), delete_after=config.deltimer)
        elif self.logs[GID]["user"] == True:
            self.logs[GID]["user"] = False
            with open("./data/settings/logs.json", "w") as e:
                json.dump(self.logs, e)
                await ctx.send(embed=lib.Editable_S("User logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def join(self, ctx):
        GID = str(ctx.guild.id)
        if self.logs[GID]["join"] == False:
            self.logs[GID]["join"] = True
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S("Join logs are now enabled", "", "Logs"), delete_after=config.deltimer)
        elif self.logs[GID]["join"] == True:
            self.logs[GID]["join"] = False
            with open("./data/settings/logs.json", "w") as e:
                json.dump(self.logs, e)
                await ctx.send(embed=lib.Editable_S("Join logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def leave(self, ctx):
        GID = str(ctx.guild.id)
        if self.logs[GID]["leave"] == False:
            self.logs[GID]["leave"] = True
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S("Leave logs are now enabled", "", "Logs"), delete_after=config.deltimer)
        elif self.logs[GID]["leave"] == True:
            self.logs[GID]["leave"] = False
            with open("./data/settings/logs.json", "w") as e:
                json.dump(self.logs, e)
                await ctx.send(embed=lib.Editable_S("Leave logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def server(self, ctx):
        GID = str(ctx.guild.id)
        if self.logs[GID]["server"] == False:
            self.logs[GID]["server"] = True
            with open("./data/settings/logs.json", "w") as f:
                json.dump(self.logs, f)
                await ctx.send(embed=lib.Editable_S("Server logs are now enabled", "", "Logs"), delete_after=config.deltimer)
        elif self.logs[GID]["server"] == True:
            self.logs[GID]["server"] = False
            with open("./data/settings/logs.json", "w") as e:
                json.dump(self.logs, e)
                await ctx.send(embed=lib.Editable_S("Server logs are now disabled", "", "Logs"), delete_after=config.deltimer)

    @toggle.group(invoke_without_command=True, name="all")
    @commands.check(check.is_moderator)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _all(self, ctx):
        GID = str(ctx.guild.id)
        self.logs[GID]["delete"] = True
        self.logs[GID]["edit"] = True
        self.logs[GID]["user"] = True
        self.logs[GID]["join"] = True
        self.logs[GID]["leave"] = True
        self.logs[GID]["server"] = True
        with open("./data/settings/logs.json", "w") as f:
            json.dump(self.logs, f)
            await ctx.send(embed=lib.Editable_S("All logs are now enabled", "", "Logs"), delete_after=config.deltimer)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        GID = str(message.guild.id)
        if GID in self.logs:
            if self.logs[GID]['delete'] == True:
                if not message.author is message.author.bot:
                    channel = self.logs[GID]["Channel"]
                    time = datetime.datetime.utcnow()
                    cleanmsg = message.content
                    for i in message.mentions:
                        cleanmsg = cleanmsg.replace(i.mention, str(i))
                    fmt = '%H:%M:%S'
                    name = message.author
                    name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                    delmessage = discord.Embed(
                    colour=0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                    infomessage = "A message by __{}__, was deleted in {}".format(message.author.nick if message.author.nick else message.author.name, message.channel.mention)
                    delmessage.add_field(name="Info:", value=infomessage, inline=False)
                    delmessage.add_field(name="Message:", value=cleanmsg)
                    delmessage.set_footer(text="User ID: {}".format(message.author.id))
                    delmessage.set_author(name="Deleted Message", url="http://i.imgur.com/fJpAFgN.png")
                    delmessage.set_thumbnail(url="http://i.imgur.com/fJpAFgN.png")
                    try:
                        sendto = guild.get_channel(int(channel))
                        await sendto.send(embed=delmessage)
                    except:
                        pass
                else:
                    pass
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            GID = str(after.id)
        except error as e:
            return
        if GID in self.logs:
            if self.logs[GID]['edit'] == True:
                cleanbefore = before.content
                for i in before.mentions:
                    cleanbefore = cleanbefore.replace(i.mention, str(i))
                cleanafter = after.content
                for i in after.mentions:
                    cleanafter = cleanafter.replace(i.mention, str(i))
                channel = self.logs[GID]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                name = before.author
                name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                try:
                    edit = discord.Embed(
                    colour=0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                    infomessage = "A message by __{}__, was edited in {}".format(before.author.nick if before.author.nick else before.author.name, before.channel.mention)
                    edit.add_field(name="Info:", value=infomessage, inline=False)
                    edit.add_field(name="Before Message:", value=cleanbefore, inline=False)
                    edit.add_field(name="After Message:", value=cleanafter)
                    edit.set_footer(text="User ID: {}".format(before.author.id))
                    edit.set_author(name="Edited Message", url="http://i.imgur.com/Q8SzUdG.png")
                    edit.set_thumbnail(url="http://i.imgur.com/Q8SzUdG.png")
                    send_to = before.guild.get_channel(channel)
                    await send_to.send(embed=edit)
                except Exception as e:
                    return
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        GID = str(member.guild.id)
        if GID in self.logs:
            if self.logs[GID]['join'] == True:
                channel = self.logs[GID]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                users = len([e.name for e in member.guild.members])
                name = member
                name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                joinmsg = discord.Embed(colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
                infomessage = "__{}__ has joined the server.".format(member.nick if member.nick else member.name)
                joinmsg.add_field(name="Info:", value=infomessage, inline=False)
                joinmsg.set_footer(text="User ID: {}".format(member.id))
                joinmsg.set_author(name="Someone Joined")
                joinmsg.set_thumbnail(url="http://www.emoji.co.uk/files/twitter-emojis/objects-twitter/11031-inbox-tray.png")
                send_to = member.guild.get_channel(channel)
                await send_to.send(embed=joinmsg)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        GID = str(member.guild.id)
        if GID in self.logs:
            if self.logs[GID]['leave'] == True:
                channel = self.logs[GID]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = "%H:%M:%S"
                users = len([e.name for e in member.guild.members])
                name = member
                name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                leave = discord.Embed(colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
                infomessage = "__{}__ has left the server.".format(member.nick if member.nick else member.name)
                leave.add_field(name="Info:", value=infomessage, inline=False)
                leave.set_footer(text="User ID: {}".format(member.id))
                leave.set_author(name="Someone Left")
                leave.set_thumbnail(url="http://www.emoji.co.uk/files/mozilla-emojis/objects-mozilla/11928-outbox-tray.png")
                send_to = member.guild.get_channel(channel)
                await send_to.send(embed=leave)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        GID = str(after.id)
        if GID in self.logs:
            if self.logs[GID]['server'] == True:
                channel = self.logs[GID]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                try:
                    if before.name != after.name:
                        sname = discord.Embed(colour=0x9bf442,
                        timestamp=datetime.datetime.utcnow()
                        )
                        before = f"**{before.name}**"
                        after = f"**{after.name}**"
                        sname.add_field(name="Before:", value=before, inline=False)
                        sname.add_field(name="After:", value=after, inline=False)
                        sname.set_footer(text="Server ID: {}".format(GID))
                        sname.set_author(name="Server Name Changed")
                        send_to = before.guild.get_channel(channel)
                        await send_to.send(embed=sname)
                    if before.region != after.region:
                        rname = discord.Embed(colour=0x9bf442,
                        timestamp=datetime.datetime.utcnow()
                        )
                        before = f"**{before.region}**"
                        after = f"**{after.region}**"
                        rname.add_field(name="Before:", value=before, inline=False)
                        rname.add_field(name="After:", value=after, inline=False)
                        rname.set_footer(text="Server ID: {}".format(GID))
                        rname.set_author(name="Server Region Changed")
                        send_to = before.guild.get_channel(channel)
                        await send_to.send(embed=rname)
                except Exception as e:
                    return
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        GID = str(after.id)
        if GID in self.logs:
            if self.logs[GID]['user'] == True:
                channel = self.logs[GID]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                if not before.nick == after.nick:
                    name = before
                    name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                    updmessage = discord.Embed(colour=0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                    infomessage = "__{}__'s nickname has changed".format(before.name)
                    updmessage.add_field(name="Info:", value=infomessage, inline=False)
                    updmessage.add_field(name="Nickname Before:", value=before.nick)
                    updmessage.add_field(name="Nickname After:", value=after.nick)
                    updmessage.set_footer(text="User ID: {}".format(before.id))
                    updmessage.set_author(name="Nickname Changed")
                    send_to = before.guild.get_channel(channel)
                    await send_to.send(embed=updmessage)
            else:
                return
        else:
            return

# Logs End ---------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.group(invoke_without_command=True)
    @commands.check(check.is_moderator)
    async def warn(self, ctx, user: discord.User = None, *args):
        GID = str(ctx.guild.id)
        if self.warn_exists(GID):
            if user:
                UID = str(user.id)
                if self.user_exists(UID, GID):
                    reason = ' '.join(args)
                    if reason == "":
                        await ctx.send(embed=lib.Editable_S(f"{user.name} was warned", f"{user.mention} Recieved a warning from {ctx.author.name}", "Warnings"), delete_after=config.deltimer)
                        self.add_warn(GID, UID)
                    else:
                        await ctx.send(embed=lib.Editable_S(f"{user.name} was warned", f"{user.mention} Recieved a warning from {ctx.author.name} for {reason}", "Warnings"), delete_after=config.deltimer)
                        self.add_warn(GID, UID)
                else:
                    self.create_record(GID, user)
                    await ctx.reinvoke()
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"{ctx.prefix}warn @someone (reason)\n{ctx.prefix}warn get @someone\n{ctx.prefix}warn remove @someone (amount)", "Usage"), delete_after=config.deltimer)
        else:
            self.warn_create(GID)
            await ctx.reinvoke()

    @warn.group()
    @commands.check(check.is_moderator)
    async def get(self, ctx, user: discord.User = None):
        GID = str(ctx.guild.id)
        if self.warn_exists(GID):
            if user:
                UID = str(user.id)
                if self.user_exists(UID, GID):
                    await ctx.send(embed=lib.Editable_S(f"{user.name} has {self.get_warns(GID, UID)}warning(s)", "", "Warnings"), delete_after=config.deltimer)
                else:
                    await ctx.send(embed=lib.Editable_S(f"{user.name} has no warnings!", "", "Warnings"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}warn get @someone", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Warnings arent enabled", f"Run {ctx.prefix}warn to begin", "Warnings"), delete_after=config.deltimer)

    @warn.group()
    @commands.check(check.is_moderator)
    async def remove(self, ctx, user: discord.User = None, num:int=0):
        GID = str(ctx.guild.id)
        if self.warn_exists(GID):
            if user and num:
                UID = str(user.id)
                if self.user_exists(UID, GID):
                    if self.enough_warns(GID, UID, num):
                        await ctx.send(embed=lib.Editable_E(f"Removed {num} warnings from {user.name}", "", "Usage"), delete_after=config.deltimer)
                        self.del_warn(GID, UID, num)
                    else:
                        await ctx.send(embed=lib.Editable_E("User does not have enough warnings", f"", "Error"), delete_after=config.deltimer)
                else:
                    await ctx.send(embed=lib.Editable_E("User has no warnings", f"", "Error"), delete_after=config.deltimer)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments", f"Usage Example:\n\n{ctx.prefix}warn remove @someone (amount)", "Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Warnings arent enabled", f"Run {ctx.prefix}warn to begin", "Error"), delete_after=config.deltimer)


    def warn_exists(self, GID):
        if sql.tableCheck("devolution_warnings", GID):
            return True

    def user_exists(self, UID, GID):
        if self.warn_exists(GID):
            if sql.Entry_Check(UID, "USERID", "devolution_warnings", GID):
                return True

    def warn_create(self, GID):
        GID = str(GID)
        mydb = sql.createConnection("devolution_warnings")
        query = (f"CREATE TABLE `devolution_warnings`.`{GID}` (USERID VARCHAR(32), name VARCHAR(32), count INT(5))")
        cur = mydb.cursor()
        cur.execute(query)
        self.log(f"Warnings Table Created for {GID}")

    def create_record(self, GID, user):
        GID = str(GID)
        UID = (user.id)
        if not self.user_exists(UID, GID):
            mydb = sql.createConnection("devolution_warnings")
            cur = mydb.cursor()
            cur.execute(f"INSERT into `devolution_warnings`.`{GID}` VALUES ('{user.id}', '{user.name}', 0)")
            mydb.commit()
            self.log(f"Warnings Profile Created for {user.id} in {GID}")
            return True
        else:
            return False

    def get_warns(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if self.user_exists(UID, GID):
            warns = str(sql.Fetch("count", "devolution_warnings", str(GID), "USERID", str(UID)))
            return warns.replace(",", " ")

    def add_warn(self, GID, UID):
        UID = str(UID)
        if self.user_exists(UID, GID):
            warns = self.get_warns(GID, UID)
            nwarns = int(warns) + 1
            mydb = sql.createConnection("devolution_warnings")
            cur = mydb.cursor()
            cur.execute(f"UPDATE `devolution_warnings`.`{GID}` SET count = {nwarns} WHERE USERID = {UID}")
            self.log(f"Warnings Updated for {UID} in {GID}: {warns} -> {nwarns}")
            mydb.commit()
        else:
            return False

    def enough_warns(self, GID, UID, num):
        UID = str(UID)
        num = int(num)
        warns = int(self.get_warns(GID, UID))
        if (warns - num) >= int(0):
            return True
        else:
            return False

    def del_warn(self, GID, UID, num):
        UID = str(UID)
        num = int(num)
        if self.user_exists(UID, GID):
            warns = int(self.get_warns(GID, UID))
            nwarns = warns - num
            mydb = sql.createConnection("devolution_warnings")
            cur = mydb.cursor()
            cur.execute(f"UPDATE `devolution_warnings`.`{GID}` SET count = {nwarns} WHERE USERID = {UID}")
            self.log(f"Warnings Updated for {UID} in {GID}: {warns} -> {nwarns}")
            mydb.commit()
        else:
            return False

    def log(self, message):
        file = open("./utils/logs/Warnings.log","a")
        file.write("[{}]: {} \n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (GMT)"), message))
        file.close()

    async def punish_create(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="punished")
        if not role in ctx.guild.roles:
            channel = ctx.channel
            await ctx.send(embed=lib.Editable_E("Punished Role not found. Creating...", "", "Error"), delete_after=config.deltimer)
            await ctx.guild.create_role(name="punished"),
            await asyncio.sleep(5)
            pass
        await ctx.send(embed=lib.Editable_S("Setting Role & Channel Permissions", "", "50% Completed"), delete_after=config.deltimer)
        if not role in ctx.guild.roles:
        for channel in ctx.guild.channels:
            role = discord.utils.get(channel.guild.roles, name="punished")
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.send_tts_messages = False
            overwrite.add_reactions = False
            await channel.set_permissions(role, overwrite=overwrite),
        await asyncio.sleep(5)
        await ctx.send(embed=lib.Editable_S("All permissions have been set.", "", "100% Completed"), delete_after=config.deltimer)


def setup(bot):
    bot.add_cog(Moderation(bot))
