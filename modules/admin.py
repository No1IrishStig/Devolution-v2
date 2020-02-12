import discord
import json
import os

from utils.functions import func
from discord.ext import commands
from utils.functions.func import lib
from utils.functions.checks import check

config = func.get("utils/config.json")

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(checks.is_owner)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cog(self, ctx):
        await ctx.send(embed=lib.Editable_E("Invalid Arguments", "Options:\n\n**load** - loads named cog.\n **unload** - Unloads named cog.\n **list** - Lists all cogs.", "Cog Usage"), delete_after=config.deltimer)

    @cog.group(invoke_without_command=True)
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def load(self, ctx, cog : str=None):
        if cog:
            try:
                self.bot.load_extension(f"modules.{cog}")
                await ctx.send(embed=lib.Editable_S(f"{cog} has been loaded.", "", "Cogs"), delete_after=config.deltimer)
            except Exception as error:
                await ctx.send(embed=lib.Editable_E(f"{cog} failed to loaded.", "", "Error"), delete_after=config.deltimer)
                func.log(error)
        else:
            await ctx.send(embed=lib.Editable_E("Please name a cog to load.", "", "Error"), delete_after=config.deltimer)

    @cog.group(invoke_without_command=True)
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unload(self, ctx, cog : str=None):
        if cog:
            try:
                self.bot.unload_extension(f"modules.{cog}")
                await ctx.send(embed=lib.Editable(f"{cog} was unloaded.", "", "Cogs"), delete_after=config.deltimer)

            except Exception as error:
                await ctx.send(embed=lib.Editable_E(f"{cog} failed to unload.", "", "Error"), delete_after=config.deltimer)
                func.log(error)

        else:
            await ctx.send(embed=lib.Editable_E("Please name a cog to unload.", "", "Error"), delete_after=config.deltimer)

    @cog.group(invoke_without_command=True)
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def list(self, ctx):
        cogs = []
        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                cogs.append(name)
        await ctx.send(embed=lib.Editable("Available Cogs", ", ".join(cogs), "Cogs"), delete_after=config.deltimer)

    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def reload(self, ctx):
        await ctx.send("Reloading...")
        os.system("cls")
        os.system("python3 bot.py")
        await self.bot.logout()

    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def shutdown(self, ctx):
        await ctx.send(embed=lib.Editable("Self Destruct Initiation Detected.. Shutting down!", "", "Signing Off"))
        await self.bot.logout()

    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def leaveid(self, ctx, id:int=None):
        if id:
            guild = self.bot.get_guild(id)
            await ctx.send(embed=lib.Editable(f"I left the guild '{guild}'", "", f"{guild}"), delete_after=config.deltimer)
            await guild.leave()
        else:
            await ctx.send(embed=lib.Editable_E("I require a Guild ID to leave", "", "Error"), delete_after=config.deltimer)


    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def activity(self, ctx, activity:str=None, *args):
        listening = discord.ActivityType.listening
        watching = discord.ActivityType.watching
        game = ' '.join(args)
        if activity == "playing" or activity == "listening" or activity == "watching":
            if not game == "":
                suc = await ctx.send(embed=lib.Editable(f"I am now {activity} {game}", "", "Playing"), delete_after=config.deltimer)
                if activity == "playing":
                    await lib.sp(self, ctx, game)
                elif activity == "listening":
                    await lib.sa(self, ctx, listening, game)
                elif activity == "watching":
                    await lib.sa(self, ctx, watching, game)
            else:
                await ctx.send(embed=lib.Editable_E("Invalid Arguments: Please enter a valid activity", "Usage Examples:\n\n**playing {name}**\n**listening {name}**\n**watching {name}**", "Activity Usage"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Invalid Arguments: Please enter a valid activity", "Usage Examples:\n\n**playing {name}**\n**listening {name}**\n**watching {name}**", "Activity Usage"), delete_after=config.deltimer)


    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def pm(self, ctx, user : discord.User=None, *args):
        if user:
            message = ' '.join(args)
            if not game == "":
                try:
                    embed = discord.Embed(
                        title = f"You've recieved a message from {ctx.author}",
                        colour = 0x9bf442,
                        )
                    embed.set_author(name=f"Message from {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    embed.add_field(name="Message:", value=message, inline=True)
                    embed.set_footer(text=f"UserID: {ctx.author.id}")
                    await user.send(embed=embed)
                except Exception as error:
                        await ctx.send(embed=lib.Editable_E("Message failed to send.", "", "Error"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Please @someone and message to DM", "", "Error"), delete_after=config.deltimer)

    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def pmid(self, ctx, id=None, *args):
        if id:
            message = ' '.join(args)
            if not message == "":
                try:
                    user = await self.bot.fetch_user(id)
                    embed = discord.Embed(
                        title = f"You've recieved a message from {ctx.author}",
                        colour = 0x9bf442,
                        )
                    embed.set_author(name=f"Message from {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    embed.add_field(name="Message:", value=message, inline=True)
                    embed.set_footer(text=f"UserID: {ctx.author.id}")
                    await user.send(embed=embed)
                except Exception as error:
                    await ctx.send(embed=lib.Editable_E("Message failed to send.", "", "Error"), delete_after=config.deltimer)
        else:
            await ctx.send(embed=lib.Editable_E("Please give me an ID and message to DM", "", "Error"), delete_after=config.deltimer)

    @commands.command()
    @commands.check(check.is_admin)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def guilds(self, ctx):
        guild = self.bot.guilds
        await ctx.author.send(embed=lib.Editable(f"Guild Count {len(self.bot.guilds)}", "{}".format(*guild.id, sep='\n'), "Guilds"), delete_after=config.deltimer)


def setup(bot):
    bot.add_cog(Admin(bot))
