from agent.action.alarm.firebase_request import send_to_firebase
from agent.action.count.exercise_counter import exercise_counter

class ActionUsecase:

    async def send_alarm(self, alarm_data: dict):

        return await send_to_firebase(alarm_data)

    # 카운터 관련 메소드
    def send_exercise_counter(self, action_data: dict):

        return exercise_counter(action_data)

