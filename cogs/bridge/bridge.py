import discord
import re
from discord import SyncWebhook
from discord.ext import commands
from javascript import On
from config import WEBHOOK_URL, CHANNEL_ID


class Bridge(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Send messages to Discord
        @On(self.client.bot, "chat")
        def handle_message(this, username, message, *args):
            webhook = SyncWebhook.from_url(WEBHOOK_URL)

            if username == 'Guild' and message.split(' ')[0] != str(self.client.bot.username):
                # Guild Message
                if message.split(' ')[-1] not in ["joined.", "left."]:
                    print(f'[MC] {username} {message}')
                    match = re.search(r"^(?:\[(?P<rank>.+?)\])?\s?(?P<player>.+?)\s?(?:\[(?P<guild_rank>.+?)\])?: (?P<message>.*)$", message)
                    username = match.group('player')
                    webhook.send(f"{match.group('message')}", username=f"{username}",
                                 avatar_url=f"https://mc-heads.net/avatar/{match.group('player')}")

                # Member Joined / Left
                elif message.split(' ')[-1] in ["joined.", "left."]:
                    colour = discord.Colour.green() if message.split(' ')[-1] == "joined." else discord.Colour.red()
                    embed = discord.Embed(colour=colour, description=f"{message}")
                    username = message.split(' ')[0]
                    webhook.send(embed=embed, username=username,
                                 avatar_url=f"https://mc-heads.net/avatar/{message.split(' ')[0]}")

    # Send messages to Minecraft
    @commands.Cog.listener()
    async def on_message(self, message):
        # Regular Messages
        if str(message.channel.id) == f'{CHANNEL_ID}' and message.author.bot is False:
            print(f"[D] {message.author.display_name}: {message.content}")
            self.client.bot.chat(f"/gc {message.author.display_name}: {message.content}")


async def setup(client):
    await client.add_cog(Bridge(client))
