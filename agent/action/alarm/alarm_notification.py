import logging

async def alarm_notification(user_id: int, action_data: dict) -> dict:
    alarm_time = action_data.get("time")
    if not alarm_time:
        return {"response": "알람 시간을 설정해주세요.", "follow_up_needed": True}

    # 이곳에서 DB에 user_id 및 alarm_time 저장 로직 추가 가능
    logging.info(f"User {user_id}의 알람이 설정되었습니다. 시간: {alarm_time}")

    return {
        "response": f"User {user_id}: 알람이 설정되었습니다. 시간: {alarm_time}",
        "follow_up_needed": False,
    }
