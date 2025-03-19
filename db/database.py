import os
import motor.motor_asyncio

# Setup the database with the mongodb uri in the env
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("URI"))

def get_database():
    """Function that returns the database, and the config collection"""
    db = client["TranslateBot"]
    config_collection = db["config"]
    return db, config_collection