import datetime
import asyncio
import discord
import json
import os

from discord.ext import commands
from collections import namedtuple

version = "v2.0.0"
JSON_FILES = ['settings/logs.json']
ERRORS = ["deltimer", "logs", "leveling"]

def get(file):
    try:
        with open(file, encoding="utf8") as data:
            return json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

with open("./utils/config.json", encoding="utf8") as data:
    config = json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))

def log(error):
    file = open("./utils/logs/Devolution.log","a")
    file.write("[{}]: {} \n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (GMT)"), error))
    file.close()

def JSON_VALIDATION():
    check = os.path.exists(f"data/settings/logs.json")
    if check is False:
        logset = open("data/settings/logs.json","w+")
        logset.write("{}")
        logset.close

    if check is False:
        print("JSON Files Generated")

def cfg_file():
    with open("./utils/config.json") as f:
        settings = json.load(f)
        print("You're missing information from your CFG file. Please fill this out and retry.")
        os.system("PAUSE")


class lib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def NoPerm():
        embed = discord.Embed(
            title = "Error!",
            description = "You dont have permission to do that!",
            colour = 0xd42c2c,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text=f"Devolution - Access Denied", icon_url="https://img.no1irishstig.co.uk/yjziv.jpg")

        return embed

    def Editable(title, desc, footer):
        embed = discord.Embed(
            title = title,
            description = desc,
            colour = 0xeb8034,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text=f"Devolution - {footer}")
        embed.set_author(name="Devolution", icon_url="https://img.no1irishstig.co.uk/yjziv.jpg")

        return embed

    def Editable_E(title, desc, footer):
        embed = discord.Embed(
            title = title,
            description = desc,
            colour = 0xd42c2c,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text=f"Devolution - {footer}")
        embed.set_author(name="Devolution", icon_url="https://img.no1irishstig.co.uk/yjziv.jpg")

        return embed

    def Editable_S(title, desc, footer):
        embed = discord.Embed(
            title = title,
            description = desc,
            colour = 0x37e666,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text=f"Devolution - {footer}")
        embed.set_author(name="Devolution", icon_url="https://img.no1irishstig.co.uk/yjziv.jpg")

        return embed

    async def sp(self, ctx, game):
        sp = (
        await self.bot.change_presence(activity=discord.Game(name=game)),
        )
        return sp

    async def sa(self, ctx, type, game):
        sa = (
        await self.bot.change_presence(activity=discord.Activity(type=type, name=game)),
        )
        return sa

    async def erase(ctx, name):
        erase = (
            await asyncio.sleep(int(config.deltimer)),
            await ctx.message.delete(),
            await name.delete()
            )
        return erase

def setup(bot):
    bot.add_cog(Economy(bot))
