from typing import Optional
from typing import Optional
from pydantic import BaseModel

from agent.dto.response.advice.advice_response import AdviceResponse
from agent.dto.response.alarm.alarm_response import AlarmResponse
from agent.dto.response.counter.counter_response import CounterResponse

class RecommendResponse(BaseModel):
    counter_response: Optional[CounterResponse] = None
    advice_response: Optional[AdviceResponse] = None
    alarm_response: Optional[AlarmResponse] = None
    