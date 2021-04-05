import json
import datetime
import discord

from discord.ext import commands

class AntiRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                                             action=discord.AuditLogAction.role_create):
            if i.user.bot:
                return

            if str(i.user.id) in whitelisted[str(role.guild.id)]:
                return
            try:
                await role.guild.kick(i.user, reason="protection: 創建身分組")
            except:
                pass
            await i.target.delete()
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                                             action=discord.AuditLogAction.role_delete):
            if i.user.bot:
                return

            if str(i.user.id) in whitelisted[str(role.guild.id)]:
                return
            try:
                await role.guild.kick(i.user, reason="protection: 刪除身分組")
            except:
                pass
            await i.target.clone()
            return

def setup(bot):
    bot.add_cog(AntiRole(bot))