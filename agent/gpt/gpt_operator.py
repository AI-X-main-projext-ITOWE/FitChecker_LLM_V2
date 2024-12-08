from agent.action.handle_action_type import*
from agent.gpt.history_by_user.memory.memory_manager import *
from agent.gpt.model.llm_models import *
from agent.gpt.classify.analyzer import *
from agent.gpt.history_by_user.conversation_manager import *


class GptOperator:
    def __init__(self):
        openai_api_key = get_openai_api_key()
        self.model, self.system_message = get_gpt_model("gpt-4o-mini", openai_api_key, 0.7, 1000)
        
    # 1단계 : advice or action 판단
    async def process_question(self, user_id: int, question: str) -> dict:
        system_message_str = self.system_message.content
        analyzed = await analyze(self.model, question, system_message_str)
        return analyzed

    async def request_action_llm(self, user_id: int, question: str, action_type: str, action_data: dict) -> dict:
        # 사용자별 메모리 관리
        user_history = get_Memory_manager(user_id, self.model)

        if user_history is None:
            user_history = get_langchain_model(self.model, user_id, new_content=question)
            add_memory(user_id, user_history)

        # ConversationManager 초기화
        user_history_manager = ConversationManager(user_history)

        # 대화 기록 요약 생성
        chat_summary = user_history_manager.get_summary()
        print(f"Debug: Chat Summary: {chat_summary}")

        # 액션 요청 처리
        action_result = await handle_action_request(user_id, question, action_type, action_data)

        # 대화 기록 업데이트 (필요시)
        user_history_manager.add_message(question, str(action_result))

        return action_result

    def create_llm_input(self, question: str, chat_summary: str, rag_context: str) -> str:
        llm_input = (
            f"사용자의 과거 대화 기록:\n{chat_summary or '대화 기록이 없습니다.'}\n\n"
            f"RAG에서 가져온 관련 정보:\n{rag_context or 'RAG 정보가 없습니다.'}\n\n"
            f"현재 질문:\n{question}\n\n"
            "위 정보를 바탕으로 사용자의 질문에 답변해주세요."
        )
        print(f"LLM Input: {llm_input}")
        return llm_input


    # 3단계 : RAG + 현재 질문 + 과거 질문을 GPT에 전달에서 최종 결과값 전달.
    async def request_advice_llm(self, user_id: int, question: str, rag_context: str) -> str:
        """
        사용자 질문에 대한 LLM의 답변을 요청하고, 대화 기록을 관리합니다.
        """
        # 사용자별 메모리 가져오기 또는 생성
        user_history = get_Memory_manager(user_id, self.model)

        if user_history is None:
            user_history = get_langchain_model(self.model, user_id, new_content=question)
            add_memory(user_id, user_history)

        # ConversationManager 초기화
        user_history_manager = ConversationManager(user_history)

        # 대화 기록 요약 생성
        chat_summary = user_history_manager.get_summary()
        print(f"Debug: Chat Summary: {chat_summary}")

        # LLM 입력 생성
        llm_input = self.create_llm_input(question, chat_summary, rag_context)

        # LLM 호출
        response = await self.model.agenerate([llm_input])  # 비동기 호출

        # 대화 기록 추가
        try:
            # 응답 텍스트 추출 및 처리
            ai_response = response.generations[0][0].text.strip()
            formatted_response = ai_response.replace("\n", "\\n")
            formatted_response = formatted_response.replace("\\n", "\n")

            # 대화 기록 추가
            user_history_manager.add_message(question, formatted_response)
            print(f"LLM Response: {formatted_response}")

        except Exception as e:
            print(f"Error during adding message to history: {e}")
            raise

        return formatted_response
