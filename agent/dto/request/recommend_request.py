from pydantic import BaseModel

class RecommendRequest(BaseModel):
    user_id: int
    age: int
    height: float
    weight: float
    gender: str
    question: str
