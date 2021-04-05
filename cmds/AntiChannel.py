import json
import datetime
import discord

from discord.ext import commands

class AntiChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                                                action=discord.AuditLogAction.channel_create):
            if str(i.user.id) in whitelisted[str(channel.guild.id)]:
                return
            try:
                await channel.guild.kick(i.user, reason="protection: 建立頻道")
            except:
                pass
            if i.user.id != 828511031465869312:
                await i.target.delete(reason=f"protection: 刪除用戶創建的頻道")
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await channel.clone()
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                                                action=discord.AuditLogAction.channel_delete):
            if str(i.user.id) in whitelisted[str(channel.guild.id)]:
                return
            try:
                await channel.guild.kick(i.user, reason="protection: 刪除頻道")
            except:
                pass
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == True:
            aaa = await member.guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
            embed = discord.Embed(title='偵測到機器人加入')
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='`所在伺服器`', value=f'{member.guild}', inline=True)
            embed.add_field(name='`名稱`', value=f'{member.display_name}', inline=True)
            embed.add_field(name='`驗證狀態`', value=f'{member.pending}', inline=True)
            embed.add_field(name='`機器人ID`', value=f'{member.id}', inline=True)
            embed.add_field(name='`邀請者`', value=f'{aaa[0].user.name}', inline=True)
            embed.add_field(name='`創建日期`', value=f'{member.created_at.strftime("%Y.%m.%d-%H:%M:%S (UTC)")}', inline=True)
            #{ctx.guild.owner.mention}"
            me = self.bot.get_user(593666614717841419)
            await me.send('<@593666614717841419>', embed=embed)
            await member.guild.owner.send(member.guild.owner.mention, embed=embed)

def setup(bot):
    bot.add_cog(AntiChannel(bot))