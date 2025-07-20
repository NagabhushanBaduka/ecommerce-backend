from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI") 
client = AsyncIOMotorClient(MONGO_URI)
db = client.ecommerce

async def init_db():
    await db.products.create_index("name")
    await db.products.create_index("sizes.size")