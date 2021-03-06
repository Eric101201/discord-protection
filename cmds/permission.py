import discord
import sys
import subprocess
from discord.ext import commands
from discord.ext.commands import has_permissions
from logger import log

class permission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='reload', help='重新載入 <Cog mod>')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.reload_extension(f"cmds.{extension}")
        # console message
        await log('discord.command', f"{extension} 已重新載入。")
        await ctx.send(f"`{extension} 已重新載入。`")

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='load', help='載入 <Cog mod>')
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cmds.{extension}")
        # console message
        await log('discord.command', f"{extension} 已載入。")
        await ctx.send(f"`{extension} 已載入。`")

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='unload', help='移除 <Cog mod>')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cmds.{extension}")
        # console message
        await log('discord.command', f"{extension} 已移除。")
        await ctx.send(f"`{extension} 已移除。`")

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='bye', help='關閉機器人')
    @commands.is_owner()
    async def bye(self, ctx):
        await ctx.send("`機器人關機中...`")
        # console message
        await log('discord.command', "機器人關機")
        await self.bot.close()

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='rebot', help='rebot')
    @commands.is_owner()
    async def rebot(self, ctx):
        """Restarts the bot"""
        await log('discord.command', "機器人重啟")
        await ctx.send("Restarting...")
        await self.bot.logout()
        subprocess.call([sys.executable, "bot.py"])

    @commands.command(name='kick', help='踢出使用者 <tag user> <原因>')
    @commands.has_guild_permissions(administrator=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'已踢出 {member.name} 用戶 原因: {reason}')
        await member.kick(reason=reason)

    @commands.command(name='ban', help='封鎖使用者 <tag user> <原因>')
    @commands.has_guild_permissions(administrator=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'已封鎖 {member.name} 用戶 原因: {reason}')
        await member.ban(reason=reason)

    @commands.command(name='unban', help='解除封鎖使用者 <tag user> <原因>')
    @commands.has_guild_permissions(administrator=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'解除封鎖 {user.mention} 用戶')
                return

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='clean', help='刪除文字 <刪除數量>')
    async def clean(self, ctx, amount=0):
        test = await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(
            title=f"您嘗試清除{amount}則訊息", description=f"最終清除{len(test)}則訊息", colour=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.has_guild_permissions(administrator=True)
    @commands.command(hidden=True)
    async def reply(self, ctx, chaid: int, messageId: int, tag: str, *, reply=None):
        cha = self.bot.get_channel(chaid)
        e = await cha.fetch_message(messageId)
        if tag == 'True':
            owo = await e.reply(reply, mention_author=True)
            embed = discord.Embed(title='已回覆訊息', color=discord.Colour.orange())
            embed.add_field(name='回復訊息連結', value=f'[點擊此處]({e.jump_url})', inline=True)
            embed.add_field(name='訊息連結', value=f'[點擊此處]({owo.jump_url})', inline=True)
            embed.add_field(name='是否tag', value=f'{tag}', inline=False)
            await ctx.send(embed=embed)
        elif tag == 'False':
            owo = await e.reply(reply, mention_author=False)
            embed = discord.Embed(title='已回覆訊息', color=discord.Colour.orange())
            embed.add_field(name='回復訊息連結', value=f'[點擊此處]({e.jump_url})', inline=True)
            embed.add_field(name='訊息連結', value=f'[點擊此處]({owo.jump_url})', inline=True)
            embed.add_field(name='是否tag', value=f'{tag}', inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(permission(bot))