from pydantic import BaseModel
from typing import Optional

class AdviceResponse(BaseModel):
    user_id: Optional[str] = None
    response: Optional[str] = None 