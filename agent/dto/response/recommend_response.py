from pydantic import BaseModel

from agent.dto.response.advice.advice_response import AdviceResponse
from agent.dto.response.alarm.alarm_response import AlarmResponse
from agent.dto.response.counter.counter_response import CounterResponse

class RecommendResponse(BaseModel):
    counter_response: CounterResponse
    advice_response: AdviceResponse
    alarm_response: AlarmResponse
