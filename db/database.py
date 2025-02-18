import os
import motor.motor_asyncio
from dotenv import load_dotenv

URI = "mongodb+srv://ytmazurex:cxsVPzwJZCnVEqrC@translatebotcluster.v7aks.mongodb.net/?retryWrites=true&w=majority&appName=TranslateBotCluster"

# client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("URI"))
client = motor.motor_asyncio.AsyncIOMotorClient(URI)

def get_database():
    db = client["TranslateBot"]
    config_collection = db["config"]
    return db, config_collection