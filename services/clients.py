from database import crm_db
from typing import List
from models.clients import Client, ClientIn
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException


async def read_clients(skip: int = 0, limit: int = 10):
    clients = []
    for client in (
        await crm_db.Clients.find().skip(skip).limit(limit).to_list(length=limit)
    ):
        clients.append(client)
    return clients


async def create_client(client: ClientIn):
    client_dict = client.dict()
    try:
        result = await crm_db.Clients.insert_one(client_dict)
        client_dict["_id"] = ObjectId(result.inserted_id)
        return client_dict
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="A client with the same name and telephone number already exists",
        )


async def read_client(client_id: str):
    client = await crm_db.Clients.find_one({"_id": ObjectId(client_id)})
    if client:
        return client
    else:
        raise HTTPException(status_code=404, detail="Client not found")


async def update_client(client_id: str, client: ClientIn):
    updated_client = await crm_db.Clients.find_one_and_update(
        {"_id": ObjectId(client_id)}, {"$set": client.dict()}, return_document=True
    )
    if updated_client:
        return updated_client
    else:
        raise HTTPException(status_code=404, detail="Client not found")


async def delete_client(client_id: str):
    deleted_client = await crm_db.Clients.find_one_and_delete(
        {"_id": ObjectId(client_id)}
    )
    if deleted_client:
        return deleted_client
    else:
        raise HTTPException(status_code=404, detail="Client not found")
