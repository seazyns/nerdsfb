import discord
import json
import requests
import time
from discord.ext import commands
from discord import SyncWebhook
from datetime import datetime
from javascript import On
from config import WEBHOOK_URL, MC_LOGS_WEBHOOK


class MessageHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

        @On(self.client.bot, "messagestr")
        def messagestr(this, message, *args):
            print(f'[MC] {message}')

            # Party Invite
            if "has invited you to join their party!" in message:
                with open("whitelist.json", "r") as f:
                    data = json.loads(f.read())
                username = message.split(' ')[1] if '[' in message.split(' ')[0] else message.split(' ')[0]

                # If username in whitelist
                if username.lower() in data['whitelist'].values():
                    self.client.bot.chat(f"/p join {username}")
                    print(f'[Frag Bot] [{str(datetime.now()).split(" ")[0]} {str(datetime.now()).split(" ")[1].split(".")[0]}] {username}')

                # If uuid in whitelist
                else:
                    api = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
                    print(f"[GET] https://api.mojang.com/users/profiles/minecraft/{username}")
                    if api['id'] in data['whitelist'].keys():
                        data['whitelist'][api['id']] = username.lower()
                        with open("whitelist.json", "w") as f:
                            f.write(json.dumps(data, indent=4))
                        self.client.bot.chat(f"/p join {username}")
                        print(f'[Frag Bot] [{str(datetime.now()).split(" ")[0]} {str(datetime.now()).split(" ")[1].split(".")[0]}] {username}')

                time.sleep(5)
                self.client.bot.chat("/p leave")
                print('Left Party')

            # Duplicate Message
            if message.lower().startswith("you cannot say the same message twice!"):
                embed = discord.Embed(colour=discord.Colour.red(), description="**You cannot send the same message twice!**")
                webhook = SyncWebhook.from_url(WEBHOOK_URL)
                webhook.send(embed=embed)

            # Player Offline
            if message.lower().startswith("that player is not online!"):
                self.client.online = False

            # Blocked
            if message.lower().startswith("you cannot message this player."):
                self.client.blocked = True

            # Direct Message
            if message.lower().startswith('from'):
                embed = discord.Embed(colour=discord.Colour.teal(), description=f"{message}")
                webhook = SyncWebhook.from_url(WEBHOOK_URL)
                webhook.send(embed=embed)
                webhook = SyncWebhook.from_url(MC_LOGS_WEBHOOK)
                webhook.send(embed=embed)

            # LOG Guild MOTD Change
            if message.lower().startswith('set line'):
                self.client.gmotd_change_embed = discord.Embed(colour=discord.Colour.teal(), description=f"```{message}```")

            # LOG Guild MOTD Preview
            if "https://discord.gg/XycFdcpgHV" in message and self.client.save_motd_preview is True:
                self.client.save_motd_preview = False
                self.client.guild_motd_preview.append(message)
            if "----------  Guild: Message Of The Day (Preview)  ----------" in message or self.client.save_motd_preview is True:
                self.client.save_motd_preview = True
                self.client.guild_motd_preview.append(message)

            # LOG Guild Online / List
            if "Total Members:" in message and self.client.save_guild_list is True:
                self.client.save_guild_list = False
            if "Guild Name: SBNOfficial" in message or self.client.save_guild_list is True:
                self.client.save_guild_list = True
                self.client.guild_list.append(message)

            if message.lower().startswith('welcome to hypixel skyblock!'):
                self.client.bot.chat("/lobby")


async def setup(client):
    await client.add_cog(MessageHandler(client))
