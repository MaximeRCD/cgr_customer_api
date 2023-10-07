from typing import Optional, Type
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls: Type['PyObjectId']):
        yield cls.validate

    @classmethod
    def validate(cls: Type['PyObjectId'], value: str, field: Field) -> 'PyObjectId':
        if not ObjectId.is_valid(value):
            raise ValueError(f"Not a valid ObjectId: {value}")
        return cls(value)


class Research(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: str
    type: str
    surface: str
    nb_piece: str
    localisation: str
    prix: str
    annonce: str
    annonce_id: str
    description: str
    image: str
    
    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {
        #     ObjectId: str
        # }

class ResearchIn(BaseModel):
    user_id: str
    type: str
    surface: str
    nb_piece: str
    localisation: str
    prix: str
    annonce: str
    annonce_id: str
    description: str
    image: str