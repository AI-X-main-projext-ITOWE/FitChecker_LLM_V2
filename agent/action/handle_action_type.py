from agent.action.alarm.alarm_notification import*
from agent.action.count.exercise_count import*
import logging


async def handle_action_request(user_id: int, question: str, action_type: str, action_data: dict) -> dict:
    """
    Action 요청 처리.
    """
    logging.debug(f"Handling Action Request: User ID={user_id}, Type={action_type}, Data={action_data}")

    if action_type == "alarm":
        return await alarm_notification(user_id, action_data)

    elif action_type == "exercise_counter":
        return await exercise_count(user_id, action_data)

    return {
        "response": f"알 수 없는 요청 유형입니다: {action_type}",
        "follow_up_needed": False,
    }
