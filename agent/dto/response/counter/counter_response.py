from typing import Optional
from pydantic import BaseModel
from typing import Optional

class CounterResponse(BaseModel):
    user_id: Optional[str] = None
    exercise: Optional[str] = None
    exercise_set: Optional[int] = None
    exercise_counter: Optional[int] = None
    response: Optional[str] = None

    