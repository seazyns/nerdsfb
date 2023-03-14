import discord
import asyncio
from discord.ext import commands
from discord import SyncWebhook
from javascript import Once, On
from config import WEBHOOK_URL


class Connections(commands.Cog):
    def __init__(self, client):
        self.client = client

        @Once(self.client.bot, "spawn")
        def spawn(this):
            embed = discord.Embed(colour=discord.Colour.green(), description="**NerdsFB Online**")
            webhook = SyncWebhook.from_url(WEBHOOK_URL)
            webhook.send(embed=embed)
            print('[Login] Successful')

        @On(self.client.bot, "disconnect")
        def disconnect(this, event):
            embed = discord.Embed(colour=discord.Colour.orange(), description="**Proxy Restarting | Restarting NerdsFB**")
            webhook = SyncWebhook.from_url(WEBHOOK_URL)
            webhook.send(embed=embed)

            async def reconnect():
                self.client.start_mineflayer()

            asyncio.run(reconnect())
            print('[Reconnect]')


async def setup(client):
    await client.add_cog(Connections(client))
