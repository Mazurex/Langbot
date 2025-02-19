import discord
import bot.settings as settings
from googletrans import Translator

translator = Translator()

def cc_to_flag(country_code: str) -> str:
    """Convert a country code into its flag variant"""
    # Some country codes (such as japanese, are different for discord emojis (ja in discord is jp))
    # To fix this, we replace these codes with custom set ones
    code_replacements = {
        "ja": "jp",
        "en": "gb",
        "ar": "iq"
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

def fix_mentions(translated: str, original: discord.message) -> str:
    """Fix discord mentions to say the users display name rather than mentioning them\n
    This fixes the issue of mutliple mentions for one message"""

    for user in original.mentions:
        translated = translated.replace(f"<@{user.id}>", f"@{user.display_name}")
        translated = translated.replace(f"@{user.id}", f"@{user.display_name}")
    return translated

def format_reply(reply_text: str,
                translated_text: str,
                message: discord.Message,
                detected_lang: str) -> str:
    """Function that formats a message based on given parameters and placeholders"""
    return reply_text.format(
            flag = cc_to_flag(detected_lang),
            translated = fix_mentions(translated_text, message),
            original = message.content,
            author_id = message.author.id,
            guild_id = message.guild.id
    )