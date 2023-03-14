import discord
import json
import requests
from discord.ext import commands
from discord import app_commands
from config import WHITELIST_PERMS


class Whitelist(commands.GroupCog, name="whitelist"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="add", description="Whitelist user to FragBot!")
    @app_commands.describe(ign="Minecraft IGN")
    async def add(self, interaction, ign: str):
        await interaction.response.defer()
        if interaction.user.id not in WHITELIST_PERMS:
            embed = discord.Embed(colour=discord.Colour.red(), description="You have no whitelist permissions!")
            await interaction.edit_original_response(embed=embed)
        else:
            with open("whitelist.json", "r") as f:
                data = json.loads(f.read())

            if ign.lower() in data['whitelist'].values():
                embed = discord.Embed(colour=discord.Colour.red(), description=f"**{ign}** is already whitelisted!")
            else:
                try:
                    api = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()
                    print(f"[GET] https://api.mojang.com/users/profiles/minecraft/{ign}")

                    data['whitelist'][api['id']] = ign.lower()
                    with open("whitelist.json", "w") as f:
                        f.write(json.dumps(data, indent=4))

                    embed = discord.Embed(colour=discord.Colour.green(), description=f"Whitelisted **{api['name']}**!")
                except Exception as e:
                    embed = discord.Embed(colour=discord.Colour.red(), description="**API Error**")

            await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="remove", description="Remove whitelist from FragBot!")
    @app_commands.describe(ign="Minecraft IGN")
    async def remove(self, interaction, ign: str):
        await interaction.response.defer()
        if interaction.user.id not in WHITELIST_PERMS:
            embed = discord.Embed(colour=discord.Colour.red(), description="You have no whitelist permissions!")
            await interaction.edit_original_response(embed=embed)
        else:
            with open("whitelist.json", "r") as f:
                data = json.loads(f.read())

            if ign.lower() in data['whitelist'].values():
                api = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()
                print(f"[GET] https://api.mojang.com/users/profiles/minecraft/{ign}")
                del data['whitelist'][api['id']]
                with open("whitelist.json", "w") as f:
                    f.write(json.dumps(data, indent=4))
                embed = discord.Embed(colour=discord.Colour.green(), description=f"Removed whitelist for **{ign}**!")
            else:
                embed = discord.Embed(colour=discord.Colour.green(), description=f"**{ign}** is not whitelisted!")
            await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Whitelist(client))
