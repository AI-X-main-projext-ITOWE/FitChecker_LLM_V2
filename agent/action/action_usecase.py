
from agent.action.alarm.alarm_usecase import send_to_firebase
from agent.action.count.exercise_counter import exercise_counter

class ActionUsecase:

    async def send_alarm(self, user_id, alarm_data: dict, fcm_token: str):
        alarm_data = {  
                        'fcm_token' : fcm_token,
                        'response' : alarm_data.get('response', ""),
                        'alarm_text' : alarm_data.get('alarm_text', ""),
                        'alarm_time' : alarm_data.get('alarm_time', "")
                      }
        
        firebase_response =  await send_to_firebase(user_id, alarm_data)

        alarm_data['alarm_id'] = firebase_response['name']      

        return alarm_data

    # 카운터 관련 메소드
    def send_exercise_counter(self, action_data: dict):

        return exercise_counter(action_data)
