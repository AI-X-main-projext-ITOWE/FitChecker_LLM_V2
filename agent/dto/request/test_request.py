from pydantic import BaseModel

class TestRequest(BaseModel):
    user_id: int
    question: str
    ragtext: str
