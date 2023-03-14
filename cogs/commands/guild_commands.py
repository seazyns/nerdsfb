import asyncio
import discord
from discord.ext import commands
from discord import app_commands


class GuildCommands(commands.GroupCog, name="guild"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="list", description="Lists guild members!")
    async def list(self, interaction):
        await interaction.response.defer()
        self.client.bot.chat("/g list")
        await asyncio.sleep(0.75)

        guild_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_list)
        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"```{guild_string}```")
        self.client.guild_list.clear()
        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, "g list")

    @app_commands.command(name="online", description="Lists guild members!")
    async def online(self, interaction):
        await interaction.response.defer()
        self.client.bot.chat("/g online")
        await asyncio.sleep(0.75)

        guild_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_list)
        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"```{guild_string}```")
        self.client.guild_list.clear()
        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, "g online")

    @app_commands.command(name="motd-preview", description="Preview guild MOTD!")
    async def motd_preview(self, interaction):
        await interaction.response.defer()
        self.client.bot.chat("/g motd preview")
        await asyncio.sleep(0.75)

        motd_preview_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_motd_preview)
        embed = discord.Embed(colour=discord.Colour.orange(),
                              description=f"```{motd_preview_string}```")
        self.client.guild_motd_preview.clear()
        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, "g motd preview")


async def setup(client):
    await client.add_cog(GuildCommands(client))
