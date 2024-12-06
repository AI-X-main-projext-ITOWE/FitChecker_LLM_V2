import logging
from agent.gpt.history_by_user.memory.memory_manager import *
from agent.gpt.model.llm_models import *
from agent.gpt.classify.analyzer import *
from agent.gpt.history_by_user.conversation_manager import *
from agent.action.handle_action_request import handle_action_request

class GptOperator:
    def __init__(self):
        openai_api_key = get_openai_api_key()
        self.model, self.system_message = get_gpt_model("gpt-4o-mini", openai_api_key, 0.7, 1000)

    async def process_question(self, user_id: int, question: str) -> dict:
        # 시스템 메시지를 문자열로 변환하여 `analyze` 함수에 전달
        system_message_str = self.system_message.content
        analyzed = await analyze(self.model, question, system_message_str)
        return analyzed

    async def request_action_llm(self, user_id: int, question: str, analyzed: dict) -> dict:
        if not analyzed.get("is_action_request"):
            return {"response": "액션 요청이 아닙니다."}

        action_type = analyzed.get("action_type")
        action_data = {"user_id": user_id, "question": question}
        return await handle_action_request(action_type, action_data)

    def create_llm_input(self, question: str, chat_summary: str, rag_context: str) -> str:
        # 사용자 메모리에서 요약을 가져오기
        llm_input = (
            f"사용자의 과거 대화 기록:\n{chat_summary}\n\n"
            f"RAG에서 가져온 관련 정보:\n{rag_context}\n\n"
            f"현재 질문:\n{question}\n\n"
            "위 정보를 바탕으로 사용자의 질문에 답변해주세요."
        )
        return llm_input

    async def request_advice_llm(self, user_id: int, question: str, rag_context: str) -> str:
        # 사용자 메모리 가져오기 또는 없으면 새로 생성하기
        user_history = get_Memory_manager(user_id, self.model)  # llm 인자를 전달하도록 수정

        # 만약 사용자의 메모리가 없다면 새로 생성하고 저장
        if user_history is None:
            user_history = get_langchain_model(self.model, user_id, new_content=question)
            add_memory(user_id, user_history)

        # ConversationManager 객체로 관리
        user_history_manager = ConversationManager(user_history)

        # 현재 질문 + 과거 질문 + RAG 정보 합쳐줌.
        chat_history = user_history_manager.get_chat_history()  # 비동기 호출이 아님으로 await 제거
        chat_summary = chat_history.get("history", "") if isinstance(chat_history, dict) else ""  # 딕셔너리 접근
        llm_input = self.create_llm_input(question, chat_summary, rag_context)
        print(f"dkdkdkdkdkdkdk{chat_summary}")
        # LLM 호출 부분 (수정된 시스템 메시지와 함께 호출)
        response = await self.model.agenerate([llm_input])
        if not response or not hasattr(response, "generations") or not response.generations:
            logging.warning("LLM 응답이 비어 있습니다. 기본값 반환.")
            return "LLM 응답이 비어 있습니다."

        ai_advice = response.generations[0][0].text.strip()

        # 대화 기록에 추가
        user_history_manager.add_message(question, ai_advice)

        return ai_advice
