import os
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
from googletrans import Translator
import asyncio

from utils.utils import format_reply
import bot.settings as settings
from db.database import get_database
from db.config_manager import get_guild_config

db, config_collection = get_database()

print(f"Database {db.name} loaded successfully!")
print(f"Collection {config_collection.name} loaded successfully!")

# Debugging mode (DEV)
DEBUG_MODE = True

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
translator = Translator()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def load_cogs():
    await bot.load_extension("commands.TranslateCmds")
    await bot.load_extension("commands.Config")

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined new guild: {guild.name} ({guild.id})")
    
    await get_guild_config(guild.id)

@bot.event
async def on_message(message: discord.Message):
    config = await get_guild_config(message.guild.id)
    
    if message.author.bot and config["IGNORE_BOTS"]:
        return
    
    detected = await translator.detect(message.content)
    if detected.lang and detected.lang not in config["IGNORE_LANGS"]:
        translated = await translator.translate(message.content, dest=config["TARGET_LANG"])
        if translated.text != message.content:
            await message.reply(format_reply(config["TRANSLATE_REPLY_MESSAGE"], translated.text, message, detected.lang))
            if DEBUG_MODE: await message.channel.send(f"**[DEBUGGING]**\n```{detected}``````{translated}```")
            print(f"Message sent by {message.author.display_name} translated in {message.channel.name}/{message.guild.name}")
    
    await bot.process_commands(message)

async def main():
    await load_cogs()
    await bot.start(os.getenv("TOKEN"))

asyncio.run(main())