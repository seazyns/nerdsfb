import discord
from discord.ext import commands
from discord import app_commands
from config import WHITELIST_PERMS


class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="exec", description="Execute a command")
    @app_commands.describe(command="Command to run")
    async def exec(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer()
        if interaction.user.id not in WHITELIST_PERMS:
            embed = discord.Embed(colour=discord.Colour.red(), description="You do not have sufficient permissions!")
        else:
            self.client.bot.chat(f"/{command}")
            await self.client.log(interaction, command)
            embed = discord.Embed(colour=discord.Colour.green(), description=f"Command Executed: **/{command}**")

        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Eval(client))
