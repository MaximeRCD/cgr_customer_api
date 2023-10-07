from typing import List, Optional, Type
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


class Criteres(BaseModel):
    localisation: List[str]
    code_postal: List[str]
    type_bien: Optional[List[str]]
    max_price: Optional[str]
    min_price: Optional[str]
    max_surface: Optional[str]
    min_surface: Optional[str]


class Client(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    telephone: str
    email: str
    criteres: Criteres
    nb_found: int
    active: bool

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}


class ClientIn(BaseModel):
    name: str
    telephone: str
    email: str
    criteres: Criteres
    nb_found: int
    active: bool
