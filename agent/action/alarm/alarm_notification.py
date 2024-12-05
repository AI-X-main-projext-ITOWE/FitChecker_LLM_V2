from datetime import datetime, timedelta

async def alarm_notification(action_data: dict) -> dict:
    alarm_time = action_data.get("time")
    message = action_data.get("message", "알람 메시지")

    if not alarm_time:
        alarm_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "response": f"알람이 설정되었습니다. 시간: {alarm_time}, 메시지: {message}",
        "follow_up_needed": False,
    }
