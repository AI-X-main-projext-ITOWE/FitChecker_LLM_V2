from pydantic import BaseModel
from typing import Optional

class AdviceResponse(BaseModel):
    response: Optional[str] = None  # 기본값 None으로 설정
