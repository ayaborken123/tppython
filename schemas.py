from typing import List, Optional
from pydantic import BaseModel

class ActorBase(BaseModel):
    actor_name: str

class ActorPublic(ActorBase):
    id: int

    class Config:
        from_attributes = True  # Remplace orm_mode


class MovieBase(BaseModel):
    title: str
    year: int
    director: str
    actors: List[ActorBase]

class MoviePublic(MovieBase):
    id: int
    actors: List[ActorPublic]

    class Config:
        from_attributes = True  # Remplace orm_mode

class SummaryRequest(BaseModel):
    movie_id: int

class SummaryResponse(BaseModel):
    summary_text: str
