import datetime
import discord
import asyncio

from discord.ext import commands
from utils.functions import func
from utils.functions.func import lib

config = func.get("utils/config.json")

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound, commands.NoPrivateMessage, commands.DisabledCommand, discord.NotFound, commands.CheckFailure)
        error = getattr(error, "original", error)

        # Bot Error's
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(embed=lib.Editable_E("Invalid Arguments", "Your command could not be processed.", "Error"), delete_after=config.deltimer)
        elif isinstance(error, commands.MissingPermissions):
            try:
                return await ctx.send(embed=lib.Editable_E("Im missing essential permissions", "", "Error"), delete_after=config.deltimer)
            except discord.Forbidden:
                return

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=lib.Editable_E(f"Calm down {ctx.author.name}, that command is cooling down.", "", "Error"), delete_after=config.deltimer)

        # Discord Error's
        elif isinstance(error, discord.Forbidden):
            try:
                return await ctx.send(embed=lib.Editable_E("I dont have permission to do that", "", "Error"), delete_after=config.deltimer)
            except discord.Forbidden:
                return
        elif isinstance(error, discord.HTTPException):
            return await ctx.send(embed=lib.Editable_E("Command Error:", f"{error}", "Error"), delete_after=config.deltimer)

        # Asyncio Error's
        elif isinstance(error, asyncio.TimeoutError):
            return await ctx.send(embed=lib.Editable_E("Request Timed Out", "", "Error"), delete_after=config.deltimer)


        errorfile = open("./utils/logs/Error.log","a")
        errorfile.write("[{}]: {} \n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (System Time)"), error))
        errorfile.close()
        print("An error has been logged.")

        raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
