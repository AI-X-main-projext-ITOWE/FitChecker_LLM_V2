from pydantic import BaseModel


class CounterResponse(BaseModel):
    exercise: str
    exercise_set: int
    exercise_counter: int