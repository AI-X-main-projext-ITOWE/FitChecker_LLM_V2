import logging
import re

async def analyze(llm, question: str):
    """
    LLM을 사용하여 질문을 분석하고 의도 파악 결과를 반환합니다.
    """
    # 프롬프트 생성
    prompt_text = (
        f"Analyze the user's request and determine its intent:\n"
        f"Question: {question}\n"
        "Classify the intent into one of the following:\n"
        "- Action request: Examples include 'Set an alarm', 'Count exercise sets'.\n"
        "- Advice request: Examples include 'I have back pain', 'Recommend exercises'.\n\n"
        "If it is an action request, specify the action type (e.g., 'alarm', 'exercise_counter').\n\n"
        "Response format:\n"
        "{'is_action_request': true/false, 'is_advice_request': true/false, 'action_type': 'type_of_action'}"
    )

    # LLM 호출
    result = await llm.agenerate([prompt_text])
    if not result or not result.generations or not result.generations[0]:
        logging.error("Invalid LLM response. No generations found.")
        return {
            "is_action_request": False,
            "is_advice_request": False,
            "action_type": None,
        }

    # 응답 텍스트 가져오기
    response_content = result.generations[0][0].text.strip() if result.generations[0] else ""
    logging.debug(f"LLM Response: {response_content}")

    # 기본값 설정
    is_action_request = "'is_action_request': true" in response_content
    is_advice_request = "'is_advice_request': true" in response_content
    action_type = None

    # Action Type 추출
    if is_action_request:
        action_type_match = re.search(r"'action_type': '(\w+)'", response_content)
        action_type = action_type_match.group(1) if action_type_match else None

    # 결과 반환
    return {
        "is_action_request": is_action_request,
        "is_advice_request": is_advice_request,
        "action_type": action_type,
    }
