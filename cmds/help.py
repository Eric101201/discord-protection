
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send('`..sos`')

def setup(bot):
    bot.add_cog(help(bot))