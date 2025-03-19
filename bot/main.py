#region Imports & Setup

import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.utils import replace_mentions, format_reply
from db.database import get_database
from db.config_manager import get_guild_config, get_channel_config
from i_logger.logger import log
from TranslationAPI.translate import translate
from bot.settings import ACTIVITY_MESSAGES

#endregion


# Bots intents (rahahahaha) >:)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(intents=intents, command_prefix="!", help_command=None)
    
    async def on_ready(self):
        log(f"Logged in as {self.user}", "critical", print_to_console=True)
        
        for guild in self.guilds:
            for role in await guild.fetch_roles():
                _ = guild.get_role(role.id)

        async def change_status():
            """Function that changes the bots status over a predefined list every set amount of time"""
            while True:
                for status in ACTIVITY_MESSAGES:
                    await self.change_presence(activity=discord.Game(name=status))
                    await asyncio.sleep(20 * 60) # 20 Minutes
        
        self.loop.create_task(change_status())
        
        try:
            synced = await self.tree.sync()
            log(f"Synced {len(synced)} slash commands", "critical")
        except Exception as e:
            log(f"Failed to sync commands: {e}", "critical")

    async def load_cogs(self):
        """Function to load all external commands"""
        await self.load_extension("commands.translate_cmds")
        await self.load_extension("commands.config")
        await self.load_extension("commands.channel_config")

    async def on_guild_join(self, guild: discord.Guild):
        log(f"Joined new guild: {guild.name} ({guild.id})")
        await asyncio.sleep(1)
        await get_guild_config(guild.id)

    async def on_guild_leave(self, guild: discord.Guild):
        log(f"Left guild: {guild.name} ({guild.id})")

    async def on_message(self, message: discord.Message):
        channel_config = await get_channel_config(message.guild.id, message.channel.id) # type: ignore
        
        if message.author.bot and channel_config["IGNORE_BOTS"]:
            return
        
        if message.author.id == self.user.id: # type: ignore
            return
        
        if not channel_config["AUTO_TRANSLATE"]:
            return

        formatted = replace_mentions(message, message.content)
        translated, detected = translate(formatted, channel_config["TARGET_LANG"])

        if detected and detected not in channel_config["IGNORE_LANGS"]:
            def contains_ignored() -> bool:
                """A function
                that returns true
                if a given string is equal to an item in a list of ignored terms otherwise false"""
                for ignored in channel_config["IGNORED_TERMS"]:
                    if ignored.lower() == translated.lower() or ignored.lower() == formatted.lower():
                        return True
                return False

            if not contains_ignored():
                if translate is None:
                    log(f"{detected} is not a valid language to translate!", "critical")
                else:
                    if translated.lower() != message.content.lower() and not any(role.id in channel_config["BLACKLISTED_ROLES"] for role in message.author.roles): # type: ignore
                        log(f"Message sent by {message.author.display_name} translated in {message.channel.name}/{message.guild.name}", "command") # type: ignore
                        
                        formatted_reply = format_reply(channel_config["TRANSLATE_REPLY_MESSAGE"], translated, message, detected)
                        
                        if channel_config["REPLY"]:
                            await message.reply(formatted_reply)
                        else:
                            await message.channel.send(formatted_reply)
        
        await self.process_commands(message)

    async def run_bot(self, token: str):
        await self.load_cogs()
        await self.start(token)


asyncio.run(Bot().run_bot(os.getenv("TOKEN"))) # type: ignore