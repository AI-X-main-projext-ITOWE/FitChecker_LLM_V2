from agent.gpt.history_by_user.memory.memory_manager import *
from agent.gpt.model.llm_models import *
from agent.gpt.classify.analyzer import *
from agent.gpt.history_by_user.conversation_manager import *

class GptOperator():
    def __init__(self):
        openai_api_key = get_openai_api_key()
        self.model:ChatOpenAI = get_gpt_model("gpt-4o-mini",openai_api_key, 0.7, 1000)

    async def process_question(self, question: str):
        analyzed = await analyze(self.model, question)
        return analyzed

    def create_llm_input(self, question: str, user_history: dict, rag_context: str) -> str:
        history_text = user_history.get("summary", "")  # LangChain에서 관리되는 요약
        llm_input = (
            f"사용자의 과거 대화 기록:\n{history_text}\n\n"
            f"RAG에서 가져온 관련 정보:\n{rag_context}\n\n"
            f"현재 질문:\n{question}\n\n"
            "위 정보를 바탕으로 사용자의 질문에 답변해주세요."
        )

        return llm_input

    async def request_advice_llm(self, user_id: str, question: str, rag_context: str) -> str:
        user_history = get_Memory_manager(user_id)
        user_history = get_langchain_model(self.model, user_id, new_content=question) if user_history is None else user_history

        #ConversationManager객체로 관리함.
        user_history = ConversationManager(user_history)

        # 현재 질문 + 과거 질문 + RAG정보 합쳐줌.
        llm_input = self.create_llm_input(question, await user_history.get_chat_history(), rag_context)

        response = await self.model.agenerate([{"role": "user", "content": llm_input}])
        ai_advice = response.generations[0][0].text.strip()

        user_history.add_message(question, ai_advice)

        return ai_advice
    
    

    


