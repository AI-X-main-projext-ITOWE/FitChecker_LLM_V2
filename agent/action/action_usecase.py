from agent.action.alarm.firebase_request import send_to_firebase

class ActionUsecase:

    async def send_alarm(self, alarm_data: dict):

        return await send_to_firebase(alarm_data)

