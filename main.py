import discord
import os
import asyncio
import time
from discord.ext import commands
from discord import SyncWebhook
from config import TOKEN
from javascript import require
from config import MC_LOGS_WEBHOOK
mineflayer = require('mineflayer')


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())
        self.online = True
        self.blocked = False
        self.bot = None
        self.fragbot_queue = []

        # Chat Saving
        self.save_guild_list = False
        self.guild_list = []
        self.save_motd_preview = False
        self.guild_motd_preview = []
        self.gmotd_change_embed = None

    async def start_mineflayer(self):
        self.bot = mineflayer.createBot({
            "host": 'hypixel.net',
            'username': 'NerdsFB',
            "auth": 'microsoft',
            "version": "1.8.9"
        })

    async def log(self, interaction, command):
        original_message = await interaction.original_response()
        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"**User:** {interaction.user.name}\n"
                                          f"**Command:** /{command}\n"
                                          f"**Jump to Message:** {original_message.jump_url}\n"
                                          f"**Timestamp:** <t:{str(time.time()).split('.')[0]}>")
        webhook = SyncWebhook.from_url(MC_LOGS_WEBHOOK)
        webhook.send(embed=embed, username="Command Logging", avatar_url=interaction.user.display_avatar.url)

    async def setup_hook(self):
        await self.start_mineflayer()
        for folder in os.listdir("./cogs"):
            for file in os.listdir(f"./cogs/{folder}"):
                if file.endswith(".py"):
                    await self.load_extension(f"cogs.{folder}.{file[:-3]}")

    async def on_ready(self):
        print(f"Logged in as {self.user.name} (ID: {self.user.id})!")
        game = discord.Game(name="Guild Bridge & Frag Bot")
        await self.change_presence(activity=game, status=discord.Status.online)
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} slash commands!")


async def run_bot():
    async with Client() as client:
        await client.start(TOKEN)

asyncio.run(run_bot())
