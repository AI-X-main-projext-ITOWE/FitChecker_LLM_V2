from pydantic import BaseModel

class AdviceResponse(BaseModel):
    response: str