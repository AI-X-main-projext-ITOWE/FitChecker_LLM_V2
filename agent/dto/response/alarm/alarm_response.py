from typing import Optional
from pydantic import BaseModel


class AlarmResponse(BaseModel):
    user_id: Optional[str] = None
    alarm_id: Optional[str] = None
    response : Optional[str] = None
    alarm_time: Optional[str] = None
    alarm_text: Optional[str] = None
    