import json
import logging
from typing import Dict, Any

async def analyze(llm, question: str, system_message: str) -> Dict[str, Any]:

    prompt_text = (
        f"{system_message}\n\n"
        f"Analyze the user's request and determine its intent:\n"
        f"Question: {question}\n"
        "Classify the intent into one of the following:\n"
        "- Action request: Examples include 'Set an alarm', 'Count exercise sets'.\n"
        "- Advice request: Examples include 'I have back pain', 'Recommend exercises'.\n\n"
        "If it is an action request, specify the action type (e.g., 'alarm', '알람', 'exercise_counter', '운동 카운트').\n\n"
        "If the action request is about setting an alarm, use action_type = 'alarm'.\n"
        "If the action request involves counting exercises (like sets/reps), use action_type = 'exercise_counter'.\n"
        "Response format:\n"
        "{'is_action_request': true/false, 'is_advice_request': true/false, 'action_type': 'type_of_action'}"
    )

    try:
        # LLM 호출
        response = await llm.agenerate([prompt_text])
        response_content = response.generations[0][0].text.strip()
        logging.info(f"LLM Response Content: {response_content}")

        # JSON 파싱
        response_content = response_content.replace("'", "\"")
        parsed_response = json.loads(response_content)
        logging.info(f"Parsed Response: {parsed_response}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}, Raw Response: {response_content}")
        parsed_response = {
            "is_action_request": False,
            "is_advice_request": False,
            "action_type": "unknown",
            "action_data": {},
            "advice_context": "Parsing error occurred. Unable to determine context."
        }
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        parsed_response = {
            "is_action_request": False,
            "is_advice_request": False,
            "action_type": "unknown",
            "action_data": {},
            "advice_context": "Unexpected error occurred."
        }

    return parsed_response
