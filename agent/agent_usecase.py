from .rag.rag_usecase import RagUsecase
from .gpt.gpt_operator import GptOperator
from .dto.request.recommend_request import RecommendRequest



# {
#         "is_action_request": is_action_request,
#         "is_advice_request": is_advice_request,
#         "action_type": action_type,
#     }
class AgentUsecase:
    def __init__(self):
        self.gpt_usecase = GptOperator()
        self.rag_usecase = RagUsecase()

    async def execute(self, request: RecommendRequest):
        user_id = request.user_id
        question = request.question

        # 1단계: 비동기 호출
        action_or_advice = await self.gpt_usecase.process_question(user_id, question)

        if action_or_advice.get("is_advice_request"):
            # 2단계 RAG
            rag_result = self.rag_usecase.extract_text(question)
            # 3단계 LLM 호출
            gpt_result = await self.gpt_usecase.request_advice_llm(user_id, question, rag_result)
            
            return [gpt_result, rag_result]

        elif action_or_advice.get("is_action_request"):
            return {"action": "Action logic executed"}

        else:
            return {"response": "에이전트의 역할에서 벗어나는 내용입니다."}
