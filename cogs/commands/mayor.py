import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from config import WHITELIST_PERMS
from enum import Enum


class Mayor(commands.Cog):
    def __init__(self, client):
        self.client = client

    class Mayors(Enum):
        Aatrox = "&eAatrox"
        Barry = "&bBarry"
        Cole = "Cole"
        Derpy = "&5Derpy"
        Diana = "&2Diana"
        Diaz = "Diaz"
        Finnegan = "Finnegan"
        Foxy = "&dFoxy"
        Jerry = "&6Jerry"
        Marina = "&3Marina"
        Paul = "&cPaul"
        Scorpius = "&0Scorpius"

    @app_commands.command(name="mayor", description="Mayor Guild MOTD")
    @app_commands.describe(mayor="Select a mayor")
    async def mayor(self, interaction: discord.Interaction, mayor: Mayors):
        await interaction.response.defer()
        self.client.bot.chat(f"/g motd set 2 &4Current Mayor: {mayor.value}")
        await asyncio.sleep(0.75)
        await interaction.edit_original_response(embed=self.client.gmotd_change_embed)
        self.client.gmotd_change_embed = None
        await self.client.log(interaction, f"g motd set 2 &4Current Mayor: {mayor.value}")


async def setup(client):
    await client.add_cog(Mayor(client))
