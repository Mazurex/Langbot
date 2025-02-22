import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Get the absolute path of the project root
projet_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add it to sys.path
sys.path.insert(0, projet_root)

import discord
from discord.ext import commands
from googletrans import Translator
import asyncio

from utils.utils import format_reply, replace_mentions, cover_blacklisted_terms
import bot.settings as settings
from db.database import get_database
from db.config_manager import get_guild_config, get_channel_config

db, config_collection = get_database()

print(f"Database {db.name} loaded successfully!")
print(f"Collection {config_collection.name} loaded successfully!")

# Debugging mode (DEV)
DEBUG_MODE = True

# Setup the discord bot environment
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# List of status messages the bot will go through
status_messages = [
    "with translations",
    "with over 100 languages",
    "as your interpreter",
    "and translating"
]

async def change_status():
    """Function that changes the bots status over a predefined list every set amount of time"""
    while True:
        for status in status_messages:
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(20 * 60) # 20 Minutes

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Start the status update loop
    bot.loop.create_task(change_status())
    
    try:
        # Sync all slash commands
        # Not ideal to do it every startup, but whatever
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def load_cogs():
    """Function to load all external commands"""
    await bot.load_extension("commands.translate_cmds")
    await bot.load_extension("commands.config")
    await bot.load_extension("commands.channel_config")

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined new guild: {guild.name} ({guild.id})")
    
    # Generate a default config if the guild didn't already have one
    await get_guild_config(guild.id)

@bot.event
async def on_message(message: discord.Message):
    # Get the guild's config
    config = await get_guild_config(message.guild.id)
    channel_config = await get_channel_config(message.guild.id, message.channel.id)
    
    # Only ignore this message is the author is a bot, and ignore bots is enabled in the channel/global config
    if message.author.bot and channel_config["IGNORE_BOTS"] and message.author.id != "1341595906662993920":
        return
    
    # Setup the translator environment
    translator = Translator()
    
    # Detect what language the message is in
    detected = await translator.detect(message.content)
    
    # If there is a language detected, and its a language that is not in the "ignore languages" channel/global config
    if detected.lang and detected.lang not in channel_config["IGNORE_LANGS"]:    
        # Translate the message into the desired langage specified in the config
        # Also replace all mentions with [MENTION]
        translated = await translator.translate(replace_mentions(message, message.content), dest=channel_config["TARGET_LANG"])
        
        # Only send the translated message if it is NOT the same as the original message
        # And if the user does NOT have a blacklisted role
        if translated.text.lower() != message.content.lower() and not any(role.id in channel_config["BLACKLISTED_ROLES"] for role in message.author.roles):
            print(f"Message sent by {message.author.display_name} translated in {message.channel.name}/{message.guild.name}")
            # Format the reply through another function, allowing customizability for each guild
            
            # Convert blacklisted terms into an empty string
            translated_message = cover_blacklisted_terms(translated.text, channel_config["BLACKLISTED_TERMS"])
            
            formatted_reply = format_reply(channel_config["TRANSLATE_REPLY_MESSAGE"], translated_message, message, detected.lang)
            
            # If the config option "REPLY" is true, reply to the untranslated message, otherwise just send it in the channel
            if channel_config["REPLY"]:
                await message.reply(formatted_reply)
            else:
                await message.channel.send(formatted_reply)
            # Debugging stuff
            if DEBUG_MODE: await message.channel.send(f"**[DEBUGGING]**\n```{detected}``````{translated}```")
    
    # Process commands
    # Apparently its useless, but I'm leaving it here anyway
    await bot.process_commands(message)

async def main():
    """Main bot function which loads all commands and starts the bot"""
    await load_cogs()
    await bot.start(os.getenv("TOKEN"))

# Uses asyncio to run the main function
asyncio.run(main())