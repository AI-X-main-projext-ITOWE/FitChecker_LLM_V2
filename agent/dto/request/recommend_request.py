from pydantic import BaseModel

class RecommendRequest(BaseModel):
    title: str
    description: str
