from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClient


client = AsyncIOMotorClient("mongodb://mongo:27017")
crm_db: AsyncIOMotorClient = client.get_database("CRM")
