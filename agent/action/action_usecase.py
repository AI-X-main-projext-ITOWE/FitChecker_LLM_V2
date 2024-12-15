from sched import scheduler
from agent.action.alarm.alarm_usecase import send_fcm_notification, send_to_firebase, schedule_alarm
from agent.action.count.exercise_counter import exercise_counter

class ActionUsecase:

    async def send_alarm(self, user_id, alarm_data: dict, fcm_token: str):
        alarm_data = {
                        'response' : alarm_data.get('response', ""),
                        'alarm_text' : alarm_data.get('alarm_text', ""),
                        'alarm_time' : alarm_data.get('alarm_time', "")
                      }
        
        firebase_response =  await send_to_firebase(user_id, alarm_data)
        
        alarm_data['alarm_id'] = firebase_response['name']

        # #스케줄을 통해 메시지를 저장함.
        # schedule_alarm(
        #     alarm_data['alarm_id'],
        #     alarm_data['alarm_time'],
        #     alarm_data['alarm_text'],
        #     alarm_data['response'],
        #     fcm_token
        # )        
        await send_fcm_notification(fcm_token, alarm_data['alarm_text'], alarm_data['response'])

        return firebase_response

    # 카운터 관련 메소드
    def send_exercise_counter(self, action_data: dict):

        return exercise_counter(action_data)
