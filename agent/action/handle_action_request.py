from agent.action.alarm import alarm_notification
from agent.action.count import exercise_count

async def handle_action_request(action_type: str, action_data: dict):
    if action_type == "alarm":
        return await alarm_notification(action_data)

    elif action_type == "exercise_counter":
        return await exercise_count(action_data)

    return {
        "response": f"알 수 없는 요청 유형입니다: {action_type}",
        "follow_up_needed": False,
    }
