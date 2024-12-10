import json
import logging
from typing import Dict, Any

async def analyze(llm, question: str, system_message: str) -> Dict[str, Any]:

    prompt_text = (
        f"{system_message}\n\n"
        f"Analyze the user's request and determine its intent:\n"
        f"Question: {question}\n"
        "Classify the intent into one of the following:\n"
        "- Action request: Examples include 'Set an alarm', 'Count exercise sets', '알람을 맞춰줘'.\n"
        "  Specifically for count, if the input includes '세트', '회', '번', or similar patterns (e.g., '2세트 15회'), it is likely to be an exercise_count request.\n"
        "  Include the action type (e.g., 'alarm', 'exercise_counter') and required parameters.\n"
        "- Advice request: Examples include 'I have back pain', 'Recommend exercises', '운동 추천해줘', '내 몸에 맞는 운동 알려줘'.\n"
        "  These requests seek guidance, plans, or recommendations based on the user's context.\n"
        "- Combination requests: If the question includes both action and advice (e.g., 'Plan a one-hour cardio exercise and set an alarm'), classify as both and provide details accordingly.\n\n"
        "Additional considerations:\n"
        "- Pay special attention to numeric inputs and their associated units (e.g., '세트', '회'). Ensure numbers are linked to their respective units to avoid misinterpretation.\n"
        "- If both sets and reps are included (e.g., '2세트 10회'), associate the first number with sets and the second with reps.\n"
        "- Handle cases where only one number is provided (e.g., '3세트', '10회'). Assume the number is for the mentioned unit, and default other parameters as needed.\n"
        "- If no numbers are present or the input is vague (e.g., '운동 좀 하자'), set action_type to 'unknown' and action_data to {}.\n\n"
        "Examples:\n"
        "1. '2회 2세트 스쿼트 할래' -> {'sets': 2, 'reps_per_set': 2, 'exercise': '스쿼트'}\n"
        "2. '10회 푸쉬업' -> {'sets': 1, 'reps_per_set': 10, 'exercise': '푸쉬업'}\n"
        "3. '3세트 런지' -> {'sets': 3, 'reps_per_set': 0, 'exercise': '런지'} (reps_per_set은 누락 가능)\n"
        "4. '팔굽혀펴기 10번' -> {'sets': 1, 'reps_per_set': 10, 'exercise': '팔굽혀펴기'}\n"
        "5. '30분 러닝' -> {'sets': 1, 'reps_per_set': 0, 'exercise': '러닝', 'duration': '30분'}\n"
        "6. '운동할래' -> {'sets': 0, 'reps_per_set': 0, 'exercise': 'unknown'}\n"
        "7. '푸쉬업 세트 좀' -> {'sets': 'not_sure', 'reps_per_set': 'not_sure', 'exercise': '푸쉬업'}\n"
        "\n"
        "Response format:\n"
        "{'is_action_request': true/false, 'is_advice_request': true/false, 'is_combination_request': true/false, 'action_type': 'type_of_action', 'action_data': {...}, 'advice_context': 'contextual_info'}"
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
            "is_combination_request": False,
            "action_type": "unknown",
            "action_data": {},
            "advice_context": "Parsing error occurred. Unable to determine context."
        }
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        parsed_response = {
            "is_action_request": False,
            "is_advice_request": False,
            "is_combination_request": False,
            "action_type": "unknown",
            "action_data": {},
            "advice_context": "Unexpected error occurred."
        }

    return parsed_response
