from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from services import research as reseach_service
from models.research import Research, ResearchIn


research_router = APIRouter(prefix="/research", tags=["research"])


@research_router.get("/", tags=["research"], response_model=List[Research])
async def get_researches():
    return await reseach_service.read_researches()


@research_router.post("/", response_model=Research)
async def create_Research(Research: ResearchIn):
    return await reseach_service.create_research(research=Research)


@research_router.get("/{client_id}", response_model=List[Research])
async def read_Research(client_id: str):
    return await reseach_service.read_client_researches(client_id=client_id)


@research_router.put("/", response_model=Research)
async def update_Research(client_id: str, annonce_id: str, research: ResearchIn):
    return await reseach_service.update_Research(client_id, annonce_id, research)


@research_router.delete("/", response_model=Research)
async def delete_Research(research_id: str):
    return await reseach_service.delete_Research(research_id)