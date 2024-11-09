from pydantic import BaseModel, Field


class Event(BaseModel):
    id: int = Field(..., description="The id of the event")
    characters: list[str] = Field(..., description="The characters of the event")
    action: str = Field(..., description="The action of the event")
    location: str = Field(..., description="The location of the event")
    time: str = Field(..., description="The time of the event")
    category: str = Field(..., description="The category of the event")
    objects: list[str] = Field(..., description="The objects of the event")
    subjects: list[str] = Field(..., description="The subjects of the event")
    adjectives: list[str] = Field(..., description="The adjectives of the event")

