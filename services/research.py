from database import crm_db
from typing import List
from models.research import Research, ResearchIn
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException



async def read_researches(skip: int = 0, limit: int = 200):
    researchs = []
    for research in (
        await crm_db.Research.find().skip(skip).limit(limit).to_list(length=limit)
    ):
        researchs.append(research)
    return researchs


async def create_research(research: ResearchIn):
    research_dict = research.dict()
    try:
        result = await crm_db.Research.insert_one(research_dict)
        research_dict["_id"] = ObjectId(result.inserted_id)
        return research_dict
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="A research with the same name and telephone number already exists",
        )
    
async def read_client_researches(client_id: str):
    client_researches = []
    try: 
        for client_research in (await crm_db.Research.find({"user_id": client_id}).to_list(length=200)):
            client_researches.append(client_research)
        
        return client_researches
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.with_traceback())
    

async def update_Research(client_id: str, annonce_id: str, research: ResearchIn):
    updated_research = await crm_db.Research.find_one_and_update(
        {"user_id": client_id, "annonce_id":annonce_id}, {"$set": research.dict()}, return_document=True
    )
    if updated_research:
        return updated_research
    else:
        raise HTTPException(status_code=404, detail="Resarch not found")
    

async def delete_Research(research_id:str):
    deletedResearch = await crm_db.Research.find_one_and_delete(
        {"_id": ObjectId(research_id)}
    )
    if deletedResearch:
        return deletedResearch
    else:
        raise HTTPException(status_code=404, detail="research not found")
