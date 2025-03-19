import discord
import bot.settings as settings
import re
from db.config_manager import update_guild_config
from i_logger.logger import log

# Custom made translation API
from TranslationAPI.constants import LANGUAGES, FLAGS

def cc_to_flag(country_code: str) -> str:
    """Convert a country code into its flag variant"""

    if country_code in LANGUAGES.keys():
        return FLAGS.get(country_code) # type: ignore
    else:
        return "🌍"

def valid_code(code: str):
    """Validate whether the given language code is a real language code.
    Returns is_valid and the code
    If the given code is the language name, it will be converted into the code"""
    code = code.lower()
    if code not in LANGUAGES.keys():
        if code not in LANGUAGES.values():
            return False, code
        else:
            code = {v: k for k, v in LANGUAGES.items()}[code]
    return True, code

def format_reply(reply_text: str,
                translated_text: str,
                message: discord.Message,
                detected_lang: str) -> str:
    """Function that formats a message based on given parameters and placeholders"""
    return reply_text.format(
            flag = FLAGS.get(detected_lang),
            translated = translated_text,
            original = message.content,
            author_id = message.author.id,
            author_display_name = message.author.display_name,
            author_username = message.author.name,
            author_mention = message.author.mention,
            author_avatar = message.author.avatar,
            guild_id = message.guild.id, # type: ignore
            guild_name = message.guild.name, # type: ignore
            channel_id = message.channel.id,
            channel_name = message.channel.name, # type: ignore
            message_id = message.id,
            message_url = message.jump_url,
            lang_code = detected_lang,
            lang_name = LANGUAGES[detected_lang].capitalize()
    )

def replace_mentions(message: discord.Message, content: str) -> str:
    """Replace all mentions with [MENTION]"""
    for user in message.mentions:
        content = re.sub(f"<@!?{user.id}>", "[MENTION]", content)
    return content

def internal_print_log_message(interaction, command_name = "UNKNOWN") -> None:
    """Function that prints on command usage"""
    log(f"{interaction.user.display_name} used the {command_name} command in {interaction.channel.name}/{interaction.guild.name}", "command")

#region Command Functions

async def f_translation_reply_message(value: str, interaction: discord.Interaction, supress: bool = False) -> str:
    await update_guild_config(interaction.guild_id, "TRANSLATE_REPLY_MESSAGE", value) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/translation-reply-message")
    return value

async def f_target_lang(value: str, interaction: discord.Interaction, supress: bool = False) -> str:
    # Clean the value, making it lowercase and stripped
    value = value.lower().strip()
    
    is_valid, value = valid_code(value)

    if not is_valid:
        return await interaction.followup.send(f"`{value}` is an invalid language, use the `/supported` command to view all valid languages") # type: ignore

    await update_guild_config(interaction.guild_id, "TARGET_LANG", value) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/target-language")
    return value

async def f_ignore_langs(value: str, interaction: discord.Interaction, supress: bool = False) -> list:
    # Make the value lowercase, stripped, and replacing any spaces with empty characters 
    if value == "nothing":
        value = [] # type: ignore
    else:
        value = value.lower().strip().replace(" ", "") # type: ignore
        
        # If there are multiple languages specified
        if "," in value:
            # Convert the value into a list, separating each item by a comma
            value = value.split(",") # type: ignore
        else:
            # Only one item in the list, still convert it into a list
            value = [value] # type: ignore
        
        # Loop through the new value list
        for i, item in enumerate(value):
            is_valid, code = valid_code(item)
            if not is_valid:
                return await interaction.followup.send(f"`{item}` is not a valid language code or name", ephemeral=True) # type: ignore
            value[i] = code # type: ignore

    if supress is False: internal_print_log_message(interaction, "config/ignore-languages")
    
    # Update the database
    await update_guild_config(interaction.guild_id, "IGNORE_LANGS", value) # type: ignore
    return value # type: ignore

async def f_ignore_bots(value: bool, interaction: discord.Interaction, supress: bool = False) -> bool:
    await update_guild_config(interaction.guild_id, "IGNORE_BOTS", value) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/ignore-bots")
    return value

async def f_ignored_terms(value: str, interaction: discord.Interaction, supress: bool = False) -> list:
    if value == "nothing":
        value = [] # type: ignore
    else:
        value = value.strip()
        if "," in value:
            value = value.split(",") # type: ignore
        else:
            value = [value] # type: ignore
    await update_guild_config(interaction.guild_id, "IGNORED_TERMS", value) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/ignored-terms")
    return value # type: ignore

async def f_reply(value: str, interaction: discord.Interaction, supress: bool = False):
    await update_guild_config(interaction.guild_id, "REPLY", value) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/reply")
    return value

async def f_blacklisted_roles(value: str, interaction: discord.Interaction, supress: bool = False):
    if value == "nothing":
        valid_role_ids = []
    else:
        # Use regex to get all role ids from the message
        role_ids = re.findall(r"<@&(\d+)>", value)

        valid_role_ids = [int(role_id) for role_id in role_ids if interaction.guild.get_role(int(role_id))] # type: ignore

        if len(valid_role_ids) == 0:
            return False, None
    await update_guild_config(interaction.guild_id, "BLACKLISTED_ROLES", valid_role_ids) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/blacklisted-roles")
    return True, valid_role_ids

async def f_auto_translate(value: str, interaction: discord.Interaction, supress: bool = False):
    await update_guild_config(interaction.guild_id, "AUTO_TRANSLATE", value) # type: ignore
    if supress is False: internal_print_log_message(interaction, "config/auto-translate")
    return value

#endregion