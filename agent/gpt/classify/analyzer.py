import logging
import re

async def analyze(llm, question: str, system_message: str):
    """
    LLM을 사용하여 질문을 분석하고 의도 파악 결과를 반환합니다.
    """
    # 시스템 프롬프트와 사용자 질문을 결합하여 프롬프트 생성
    prompt_text = (
        f"{system_message}\n\n"
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
    response = await llm.agenerate([prompt_text])

    if not response or not hasattr(response, "generations") or not response.generations:
        logging.warning("LLM 결과가 비어 있습니다. 기본값 반환.")
        return {
            "is_action_request": False,
            "is_advice_request": True,
            "action_type": None,
        }

    response_content = response.generations[0][0].text.strip()
    logging.info(f"LLM Response Content: {response_content}")

    # 기본값 설정
    is_action_request = "'is_action_request': true" in response_content
    is_advice_request = "'is_advice_request': true" in response_content
    action_type = None

    # Action Type 추출
    if is_action_request:
        action_type_match = re.search(r"'action_type':\s*'(\w+)'", response_content)
        action_type = action_type_match.group(1) if action_type_match else None

    # 응답 형식 검증 및 의도 파악 실패 시 기본값 설정
    if not (is_action_request or is_advice_request):
        logging.warning("의도를 파악하지 못했으므로 기본적으로 조언 요청으로 설정합니다.")
        return {
            "is_action_request": False,
            "is_advice_request": True,
            "action_type": None,
        }

    # 결과 반환
    return {
        "is_action_request": is_action_request,
        "is_advice_request": is_advice_request,
        "action_type": action_type,
    }