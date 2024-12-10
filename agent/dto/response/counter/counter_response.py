from pydantic import BaseModel
from typing import Optional

class CounterResponse(BaseModel):
    exercise: str
    exercise_set: int
    exercise_reps_per_set: int
    response: Optional[str] = None  # Optional 필드 추가
