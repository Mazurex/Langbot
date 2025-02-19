from bot import settings

from db.database import get_database

# Get the database information from another function
db, config_collection = get_database()

def default_cfig(guild_id: str | None = None) -> dict:
    """Function that returns the default config with an optional guild_id param"""
    cfig = {
        "TRANSLATE_REPLY_MESSAGE": settings.DEFAULT_REPLY_MESSAGE,
        "TARGET_LANG": settings.DEFAULT_TARGET_LANG,
        "IGNORE_LANGS": settings.DEFAULT_IGNORE_LANGS,
        "IGNORE_BOTS": settings.DEFAULT_IGNORE_BOTS
    }
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
        print(f"Error with getting a guilds config: {e}")


async def update_guild_config(guild_id: int, key: str, value) -> None:
    """Updates a specific setting for the guild"""
    try:
        await config_collection.update_one(
            {"guild_id": guild_id},
            {"$set": {key: value}}
        )
    except Exception as e:
        print(f"Error when trying to update a guild config parameter: {e}")

async def reset_guild_config(guild_id: int) -> None:
    """Resets the guild's config to the default values"""
    try:
        await config_collection.update_one(
            {"guild_id": guild_id},
            {"$set": default_cfig()}
        )
    except Exception as e:
        print(f"Error when resetting a guilds config: {e}")