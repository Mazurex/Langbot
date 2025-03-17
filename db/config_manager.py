from bot import settings

from db.database import get_database
from i_logger.logger import log

# Get the database information from another function
db, config_collection = get_database()

def default_cfig(guild_id: str | None = None, remove_channel_config: bool = False) -> dict:
    """Function that returns the default config with an optional guild_id param"""
    cfig = {
        "TRANSLATE_REPLY_MESSAGE": settings.DEFAULT_REPLY_MESSAGE,
        "TARGET_LANG": settings.DEFAULT_TARGET_LANG,
        "IGNORE_LANGS": settings.DEFAULT_IGNORE_LANGS,
        "IGNORE_BOTS": settings.DEFAULT_IGNORE_BOTS,
        "IGNORED_TERMS": settings.DEFAULT_IGNORED_TERMS,
        "REPLY": settings.DEFAULT_REPLY,
        "BLACKLISTED_ROLES": settings.DEFAULT_BLACKLISTED_ROLES,
        "CHANNEL_CONFIG": settings.DEFAULT_CHANNEL_CONFIG,
        "AUTO_TRANSLATE": settings.DEFAULT_AUTO_TRANSLATE
    }
    
    if remove_channel_config:
        del cfig["CHANNEL_CONFIG"]
    
    if guild_id:
        # Append the guild id at the start of the dict if one is given
        cfig = {"guild_id": guild_id, **cfig}
    return cfig
    

async def get_guild_config(guild_id: int) -> dict:
    """Function that returns the config of the guild, or creates a default one and returns that"""
    try:
        # Try to find a config for that guild
        config = await config_collection.find_one({"guild_id": guild_id})
        if not config:
            # If it doesn't exist, create a new one
            config = default_cfig(guild_id)
            # Insert the new default config into the database
            await config_collection.insert_one(config)
            return config
        return config
    except Exception as e:
        log(f"Error with getting a guilds config: {e}", "critical")


async def update_guild_config(guild_id: int, key: str, value) -> None:
    """Updates a specific setting for the guild"""
    try:
        await config_collection.update_one(
            {"guild_id": guild_id},
            {"$set": {key: value}}
        )
    except Exception as e:
        log(f"Error when trying to update a guild config parameter: {e}", "critical")

async def reset_guild_config(guild_id: int) -> None:
    """Resets the guild's config to the default values"""
    try:
        await config_collection.update_one(
            {"guild_id": guild_id},
            {"$set": default_cfig()}
        )
    except Exception as e:
        log(f"Error when resetting a guilds config: {e}", "critical")

async def set_channel_config(
    guild_id: int,
    channel_id: int,
    translate_reply_message: str = None,
    target_lang: str = None,
    ignore_langs: list = None,
    ignore_bots: bool = None,
    reply: bool = None,
    blacklisted_roles: list = None,
    ignored_terms: list = None,
    auto_translate: bool = None
) -> dict:
    """Creates/Updates a channel specfic config"""
    try:
        config = await get_guild_config(guild_id)
        channel_config = config.get("CHANNEL_CONFIG", {})
        
        if str(channel_id) in channel_config:
            await remove_channel_config(guild_id, channel_id)
            channel_config = {}
                    
        if translate_reply_message is None: translate_reply_message = config.get("TRANSLATE_REPLY_MESSAGE")
        if target_lang is None: target_lang = config.get("TARGET_LANG")
        if ignore_langs is None: ignore_langs = config.get("IGNORE_LANGS")
        if ignore_bots is None: ignore_bots = config.get("IGNORE_BOTS")
        if ignored_terms is None: blacklisted_terms = config.get("IGNORED_TERMS")
        if reply is None: reply = config.get("REPLY")
        if blacklisted_roles is None: blacklisted_roles = config.get("BLACKLISTED_ROLES")
        if auto_translate is None: auto_translate = config.get("AUTO_TRANSLATE")
        
        new_config = {
            "TRANSLATE_REPLY_MESSAGE": translate_reply_message,
            "TARGET_LANG": target_lang,
            "IGNORE_LANGS": ignore_langs,
            "IGNORE_BOTS": ignore_bots,
            "IGNORED_TERMS": blacklisted_terms,
            "REPLY": reply,
            "BLACKLISTED_ROLES": blacklisted_roles,
            "AUTO_TRANSLATE": auto_translate
        }
        
        channel_config[str(channel_id)] = new_config
        await update_guild_config(guild_id, "CHANNEL_CONFIG", channel_config)
        return new_config
    except Exception as e:
        log(f"Error adding/updating channel config: {e}", "critical")

async def remove_channel_config(guild_id: int, channel_id: int) -> bool:
    """Removes a channel config and returns true if successful, otherwise false"""
    try:
        config = await get_guild_config(guild_id)
        channel_config = config.get("CHANNEL_CONFIG", {})
        
        if str(channel_id) in channel_config:
            del channel_config[str(channel_id)]
            await update_guild_config(guild_id, "CHANNEL_CONFIG", channel_config)
            return True
        return False
    except:
        return False

async def get_channel_config(guild_id: int, channel_id: int) -> dict:
    """Returns the config for a specific channel, falling back to the guild-wide config"""
    try:
        # Get the guild-based config
        config = await get_guild_config(guild_id)
        # Get the channel configs
        channel_config = config.get("CHANNEL_CONFIG", {})
        
        # Get the specific channel config
        if str(channel_id) in channel_config:
            return channel_config[str(channel_id)]
        
        # If there is no config for that channel return the guild-based config
        # Without the channel config item
        config.pop("CHANNEL_CONFIG", None)
        return config
    except Exception as e:
        log(f"Error retrieving channel config: {e}", "critical")
        return {}