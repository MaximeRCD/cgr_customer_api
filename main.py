from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from models.clients import Client
from database import client, crm_db
from routers.clients import client_router
from routers.research import research_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_router)
app.include_router(research_router)


@app.on_event("startup")
async def startup_db_client():
    try:
        client.admin.command("ping")
        print(
            "Pinged your deployment. You successfully connected to MongoDB! Choose a db"
        )
    except Exception as e:
        print(e)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()