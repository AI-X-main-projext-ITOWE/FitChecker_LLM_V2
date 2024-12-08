import json
import logging

async def analyze(llm, question: str, system_message: str):
    """
    LLM을 사용하여 질문을 분석하고 의도 파악 결과를 반환합니다.
    """
    prompt_text = (
        f"{system_message}\n\n"
        f"Analyze the user's request and determine its intent:\n"
        f"Question: {question}\n"
        "Classify the intent into one of the following:\n"
        "- Action request: Examples include 'Set an alarm', 'Count exercise sets'.\n"
        "  Include the action type (e.g., 'alarm', 'exercise_counter') and required parameters.\n"
        "- Advice request: Examples include 'I have back pain', 'Recommend exercises'.\n\n"
        "Response format:\n"
        "{'is_action_request': true/false, 'is_advice_request': true/false, 'action_type': 'type_of_action', 'action_data': {...}}"
    )

    response = await llm.agenerate([prompt_text])

    response_content = response.generations[0][0].text.strip()
    logging.info(f"LLM Response Content: {response_content}")

    try:
        # JSON 파싱
        response_content = response_content.replace("'", "\"")
        parsed_response = json.loads(response_content)
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}, Raw Response: {response_content}")
        return {
            "is_action_request": False,
            "is_advice_request": True,
            "action_type": None,
            "action_data": {}
        }

    return parsed_response