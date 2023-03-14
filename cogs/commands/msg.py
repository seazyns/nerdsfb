import discord
import asyncio
from discord.ext import commands
from discord import app_commands


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="msg", description="Messages a user!")
    @app_commands.describe(ign="Minecraft IGN")
    @app_commands.describe(message="Message to send")
    async def msg(self, interaction: discord.Interaction, ign: str, message: str):
        await interaction.response.defer()
        self.client.bot.chat(f"/msg {ign} {message}")
        await asyncio.sleep(0.75)
        if self.client.online is False:
            embed = discord.Embed(colour=discord.Colour.red(), description=f"That player is not online!")
            self.client.online = True
        elif self.client.blocked is True:
            embed = discord.Embed(colour=discord.Colour.red(), description=f"You cannot message this player.")
            self.client.blocked = False
        else:
            embed = discord.Embed(colour=discord.Colour.teal(), description=f"To **{ign}**: {message}")

        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, f"msg {ign} {message}")


async def setup(client):
    await client.add_cog(Message(client))
