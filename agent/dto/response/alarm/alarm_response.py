from pydantic import BaseModel


class AlarmResponse(BaseModel):
    alarm_id: str
    alarm_time: str
    alarm_text: str