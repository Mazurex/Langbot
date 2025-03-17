###################################################
##                                               ##
##       For the newest version of the bot       ##
##        We have made custom translation        ##
##           Instead of googletrans              ##
##                                               ##
###################################################

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add it to sys.path
sys.path.insert(0, project_root)

import discord
from discord.ext import commands
import asyncio

from utils.utils import replace_mentions, format_reply
from db.database import get_database
from db.config_manager import get_guild_config, get_channel_config

from i_logger.logger import log

# Custom made translation API
from TranslationAPI.translate import  translate
from TranslationAPI.detect import detect

db, config_collection = get_database()

log(f"Database {db.name} loaded successfully!", "critical")
log(f"Collection {config_collection.name} loaded successfully!", "critical")
# Debugging mode (DEV)
DEBUG_MODE = False

# Setup the discord bot environment
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(intents=intents, command_prefix="!", help_command=None)

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
    log(f"Logged in as {bot.user}", "critical")
    
    # Cache all roles
    for guild in bot.guilds:
        for role in await guild.fetch_roles():
            _ = guild.get_role(role.id)
    
    # Start the status update loop
    bot.loop.create_task(change_status())
    
    try:
        # Sync all slash commands
        # Not ideal to do it every startup, but whatever
        synced = await bot.tree.sync()
        log(f"Synced {len(synced)} slash commands", "critical")
    except Exception as e:
        log(f"Failed to sync commands: {e}", "critical")

async def load_cogs():
    """Function to load all external commands"""
    await bot.load_extension("commands.translate_cmds")
    await bot.load_extension("commands.config")
    await bot.load_extension("commands.channel_config")

@bot.event
async def on_guild_join(guild: discord.Guild):
    log(f"Joined new guild: {guild.name} ({guild.id})")

    # Sleep for 1 second to prevent duplication in the database
    # This sometimes gets called at the same time as on_message
    # Which also creates a default config if there isn't one,
    # So this event is really an edge-case
    await asyncio.sleep(1)
    # Generate a default config if the guild didn't already have one
    await get_guild_config(guild.id)

@bot.event
async def on_guild_leave(guild: discord.Guild):
    log(f"Left guild: {guild.name} ({guild.id})")

@bot.event
async def on_message(message: discord.Message):
    # Get the guild's config
    channel_config = await get_channel_config(message.guild.id, message.channel.id)
    
    # Only ignore this message is the author is a bot, and ignore bots is enabled in the channel/global config
    if message.author.bot and channel_config["IGNORE_BOTS"]:
        return
    
    # Bot cannot translate its own messages
    if message.author.id == bot.user.id:
        return
    
    # If the channel is set to not automaticallty translate, return
    if not channel_config["AUTO_TRANSLATE"]:
        return
    
    # Detect what language the message is in
    detected = detect(message.content).lower()
    
    # If there is a language detected, and it's a language that is not in the "ignore languages" channel/global config
    if detected and detected not in channel_config["IGNORE_LANGS"]:
        # Translate the message into the desired language specified in the config
        # Also replace all mentions with [MENTION]
        formatted = replace_mentions(message, message.content)
        translated = translate(formatted, channel_config["TARGET_LANG"])
        # Translate the message until it is fully in the target language (ensures multilanguage messages get translated properly)
        while detect(translate) != channel_config["TARGET_LANG"]:
            translated = translate(formatted, channel_config["TARGET_LANG"])
        
        def contains_ignored() -> bool:
            """A function
            that returns true
            if a given string is equal to an item in a list of ignored terms otherwise false"""
            for ignored in channel_config["IGNORED_TERMS"]:
                if ignored.lower() == translated.lower() or ignored.lower() == formatted.lower():
                    return True
            return False


        # Send the message only if it doesn't contain a ignored term
        if not contains_ignored():
            # If the value of translation is None, the detected language is not valid
            if translate is None:
                log(f"{detected} is not a valid language to translate!", "critical")
            else:
                # Only send the translated message if it is different from the original message,
                # And if the user does NOT have a blacklisted role
                if translated.lower() != message.content.lower() and not any(role.id in channel_config["BLACKLISTED_ROLES"] for role in message.author.roles):
                    log(f"Message sent by {message.author.display_name} translated in {message.channel.name}/{message.guild.name}", "command")
                    # Format the reply through another function, allowing customizability for each guild
                    formatted_reply = format_reply(channel_config["TRANSLATE_REPLY_MESSAGE"], translated, message, detected)
                    
                    # If the config option "REPLY" is true, reply to the untranslated message, otherwise send it
                    # in the channel
                    if channel_config["REPLY"]:
                        await message.reply(formatted_reply)
                    else:
                        await message.channel.send(formatted_reply)
                    # Debugging stuff
                    if DEBUG_MODE: await message.channel.send(f"**[DEBUGGING]**\n```{detected}``````{translated}```")
    
    # Process commands
    # Apparently it's useless, but I'm leaving it here anyway
    await bot.process_commands(message)

async def main():
    """Main bot function which loads all commands and starts the bot"""
    await load_cogs()
    await bot.start(os.getenv("TOKEN"))

# Uses asyncio to run the main function
asyncio.run(main())