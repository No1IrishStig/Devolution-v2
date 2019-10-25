import discord
import os

from utils.functions import sql
from discord.ext import commands
from utils.functions import func

config = func.get("utils/config.json")
bot = commands.Bot(command_prefix = (config.prefix, config.admin_prefix))
bot.remove_command('help')

if config.token == "Token" or config.admins == 0:
    func.cfg_file()

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}\nVersion: {discord.__version__}\nBuild: {func.version}')
    await bot.change_presence(activity=discord.Game(name=config.playing, type=1, url='https://github.com/No1IrishStig/'))


func.JSON_VALIDATION()
sql.Init()

for file in os.listdir("modules"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"modules.{name}")
        
bot.load_extension("utils.functions.errorhandler")
bot.run(config.token, reconnect=True)
