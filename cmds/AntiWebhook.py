import json
import datetime
import discord

from discord.ext import commands

class AntiWebhook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        async for i in webhook.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                                                action=discord.AuditLogAction.webhook_create):
            if str(i.user.id) in whitelisted[str(webhook.guild.id)]:
                return
            try:
                await webhook.guild.kick(i.user, reason="protection: 創建 Webhooks")
            except:
                pass
            await i.target.delete()
            return

def setup(bot):
    bot.add_cog(AntiWebhook(bot))