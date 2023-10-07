from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from services import clients as clients_service
from models.clients import Client, ClientIn


client_router = APIRouter(prefix="/clients", tags=["clients"])


@client_router.get("/", tags=["clients"], response_model=List[Client])
async def get_clients():
    return await clients_service.read_clients()


@client_router.post("/", response_model=Client)
async def create_client(client: ClientIn):
    return await clients_service.create_client(client=client)


@client_router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str):
    return await clients_service.read_client(client_id=client_id)


@client_router.put("/{client_id}", response_model=Client)
async def update_client(client_id: str, client: ClientIn):
    return await clients_service.update_client(client_id=client_id, client=client)


@client_router.delete("/{client_id}", response_model=Client)
async def delete_client(client_id: str):
    return await clients_service.delete_client(client_id=client_id)
