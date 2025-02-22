import discord
import bot.settings as settings
from db.config_manager import get_guild_config, update_guild_config
from googletrans import Translator, LANGUAGES, LANGCODES
import re

translator = Translator()

def cc_to_flag(country_code: str) -> str:
    """Convert a country code into its flag variant"""
    # Some country codes (such as japanese, are different for discord emojis (ja in discord is jp))
    # To fix this, we replace these codes with custom set ones
    code_replacements = {
        "ja": "jp",
        "en": "gb",
        "ar": "iq",
        "ky": "ru"
    }
    
    # If there is a - in the code, it means its a BCP 47 language tag
    # So we re-run this function, just getting the country code ending part (after the -)
    if "-" in country_code:
        return cc_to_flag(country_code.split("-")[1])

    # If the country code is in the above code_replacements
    # Then set the value to the one adjacent to the code replacements
    country_code = code_replacements.get(country_code, country_code)
    
    if len(country_code) == 2:
        return "".join(chr(127397 + ord(c)) for c in country_code.upper())
    return settings.DEFAULT_INVALID_COUNTRY_CODE_ICON

def format_reply(reply_text: str,
                translated_text: str,
                message: discord.Message,
                detected_lang: str) -> str:
    """Function that formats a message based on given parameters and placeholders"""
    return reply_text.format(
            flag = cc_to_flag(detected_lang),
            translated = translated_text,
            original = message.content,
            author_id = message.author.id,
            author_display_name = message.author.display_name,
            author_username = message.author.name,
            author_mention = message.author.mention,
            author_avatar = message.author.avatar,
            guild_id = message.guild.id,
            guild_name = message.guild.name,
            channel_id = message.channel.id,
            channel_name = message.channel.name,
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

def cover_blacklisted_terms(message: str, blacklisted: iter) -> str:
    """Replace all blacklisted terms with an empty string"""
    for item in blacklisted:
        if item in message:
            message = message.replace(item, "")
    return message

def internal_print_log_message(interaction, command_name = "UNKNOWN") -> None:
    print(f"{interaction.user.display_name} used the {command_name} command in {interaction.channel.name}/{interaction.guild.name}")

# Dupe commands (channel-config is sorta a version of config commands, to prevent duplication we make one general set of functions)

async def f_translation_reply_message(value: str, interaction: discord.Interaction, supress: bool = False) -> str:
    await update_guild_config(interaction.guild_id, "TRANSLATE_REPLY_MESSAGE", value)
    if supress is False: internal_print_log_message(interaction, "config/translation-reply-message")
    return value

async def f_target_lang(value: str, interaction: discord.Interaction, supress: bool = False) -> str:
    # Clean the value, making it lowercase and stripped
    value = value.lower().strip()
    # If the value is not a valid language code (such as "en")
    if value not in LANGUAGES.keys():
        # If the value is not a valid language name (such as "england")
        if value not in LANGCODES.keys():
            return await interaction.followup.send(f"`{value}` is an invalid language, use the `/supported` command to view all valid languages")
        else:
            # If the value is a valid country name, convert it into its key code
            value = LANGCODES.get(value)
    await update_guild_config(interaction.guild_id, "TARGET_LANG", value)
    if supress is False: internal_print_log_message(interaction, "config/target-language")
    return value

async def f_ignore_langs(value: str, interaction: discord.Interaction, supress: bool = False) -> list:
    # Make the value lowercase, stripped, and replacing any spaces with empty characters 
    value = value.lower().strip().replace(" ", "")
    
    # If there are multiple languages specified
    if "," in value:
        # Convert the value into a list, seperating each item by a comma
        value = value.split(",")
    else:
        # Only one item in the list, still convert it into a list
        value = [value]
    
    # Loop through the new value list
    for i, item in enumerate(value):
        # Item is not a language code (such as "en")
        if item not in LANGUAGES.keys():
            # Item is not a language name (such as "english")
            if item not in LANGCODES.keys():
                # Not a valid language, gracefully tell user
                return await interaction.followup.send(f"`{item}` is not a valid language code or name", ephemeral=True)
            else:
                # Convert the language name into the language code
                value[i] = LANGCODES[item]
    if supress is False: internal_print_log_message(interaction, "config/ignore-languages")
    
    # Update the database
    await update_guild_config(interaction.guild_id, "IGNORE_LANGS", value)
    return value

async def f_ignore_bots(value: bool, interaction: discord.Interaction, supress: bool = False) -> bool:
    await update_guild_config(interaction.guild_id, "IGNORE_BOTS", value)
    if supress is False: internal_print_log_message(interaction, "config/ignore-bots")
    return value

async def f_blacklisted_terms(value: str, interaction: discord.Interaction, supress: bool = False) -> list:
    value = value.strip().replace(" ", "")
    if "," in value:
        value = value.split(",")
    else:
        value = [value]
    await update_guild_config(interaction.guild_id, "BLACKLISTED_TERMS", value)
    if supress is False: internal_print_log_message(interaction, "config/blacklisted-terms")
    return value

async def f_reply(value: str, interaction: discord.Interaction, supress: bool = False):
    await update_guild_config(interaction.guild_id, "REPLY", value)
    if supress is False: internal_print_log_message(interaction, "config/reply")
    return value

async def f_blacklisted_roles(value: str, interaction: discord.Interaction, supress: bool = False):
    if value == "*":
        valid_role_ids = []
    else:
        # Use regex to get all role ids from the message
        role_ids = re.findall(r"<@&(\d+)>", value)

        valid_role_ids = [int(role_id) for role_id in role_ids if interaction.guild.get_role(int(role_id))]
        
        if len(valid_role_ids) == 0:
            return False
    
    await update_guild_config(interaction.guild_id, "BLACKLISTED_ROLES", valid_role_ids)
    if supress is False: internal_print_log_message(interaction, "config/blacklisted-roles")
    return True, valid_role_ids