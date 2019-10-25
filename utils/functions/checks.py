import datetime
import discord

from discord.ext import commands
from utils.functions import func
from utils.functions.func import lib

config = func.get("utils/config.json")

class check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_admin(ctx):
        if ctx.message.content.startswith("/"):
            if ctx.author.id in config.admins:
                await ctx.message.delete()
                file = open("./utils/logs/Admin.log","a")
                file.write("[{}]: Access Granted to {} | CMD - {}\n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (System Time)"), ctx.author.id, ctx.message.content))
                file.close()
                return True
            else:
                file = open("./utils/logs/Admin.log","a")
                file.write("[{}]: Access Denied for {} | CMD - {}\n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (System Time)"), ctx.author.id, ctx.message.content))
                file.close()
                await ctx.send(embed=lib.NoPerm())

    async def is_moderator(ctx):
        if ctx.author.id in config.admins or ctx.author.guild_permissions.kick_members:
            return True
        else:
            await ctx.send(embed=lib.NoPerm())


def setup(bot):
    bot.add_cog(Economy(bot))
