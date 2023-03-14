import discord
import asyncio
from discord.ext import commands
from discord import app_commands


class Boop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="boop", description="Boops a user!")
    @app_commands.describe(ign="Minecraft IGN")
    async def msg(self, interaction: discord.Interaction, ign: str):
        await interaction.response.defer()
        self.client.bot.chat(f"/boop {ign}")
        await asyncio.sleep(0.75)
        if self.client.online is False:
            embed = discord.Embed(colour=discord.Colour.red(), description=f"That player is not online!")
            self.client.online = True
        elif self.client.blocked is True:
            embed = discord.Embed(colour=discord.Colour.red(), description=f"You cannot message this player.")
            self.client.blocked = False
        else:
            embed = discord.Embed(colour=discord.Colour.purple(), description=f"<:boop:1083793189925822594> {ign}")

        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, f"boop {ign}")


async def setup(client):
    await client.add_cog(Boop(client))
