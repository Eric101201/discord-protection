import discord
import asyncio
import os
from logger import log
from dotenv import load_dotenv
load_dotenv()

from discord.ext import commands, tasks

intents = discord.Intents.all()

prefix = '..'
class sosCommand( commands.DefaultHelpCommand ):
  def __init__( self,**options ):
    super().__init__( **options )
    self.command_attrs["name"] = "sos"

bot = commands.Bot(command_prefix=prefix, help_command = sosCommand(), intents=intents, owner_ids="593666614717841419")

@tasks.loop(seconds=1)
async def status_task():
    await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching, name=F"{prefix}help"))
    await asyncio.sleep(5)
    await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching,name=f'我正在 {(str(len(bot.guilds)))}' + "個伺服器做奴隸"))
    await asyncio.sleep(5)

@bot.event
async def on_ready():
    await log('discord', "-"*10)
    await log('discord', "bot Loading...")
    status_task.start()
    print(">> Bot is online <<")
    print(bot.user.name)
    print(bot.user.id)
    print(f'prefix:{prefix}')
    print(str(len(bot.guilds)) + " servers")
    print('========OwO========')
    await log('discord', ">> Bot is online <<")

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)
