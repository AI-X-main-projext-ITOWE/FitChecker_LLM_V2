from pydantic import BaseModel
from typing import Optional

class RecommendRequest(BaseModel):
    user_id: str
    fcm_token: str
    age: int
    height: float
    weight: float
    gender: str
    question: Optional[str] = ""