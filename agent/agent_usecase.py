from .rag.rag_usecase import RagUsecase
from .gpt.gpt_usecase import GptUsecase
from .dto.request.recommend_request import RecommendRequest
from .action.action_usecase import *
from .action.alarm.firebase_request import *

# {
#         "is_action_request": is_action_request,
#         "is_advice_request": is_advice_request,
#         "action_type": action_type,
#     }
class AgentUsecase:
    def __init__(self):
        self.gpt_usecase = GptUsecase()
        self.rag_usecase = RagUsecase()
        self.action_usecase = ActionUsecase()

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
            # 1단계 llm에게 액션에 대한 내용을 받아옴
            action_type = action_or_advice.get("action_type")  # action_type 추출

            # 2단계 액션 타입을 분리함
            # 2-1단계
            if action_type == "alarm":
                # 3단계 LLM한테 펑션콜 코드를 받아옴.
                alarm_result = await self.gpt_usecase.call_with_function(question)
                # 4단계 펑션콜 코드를 실행해서 파이어베이스에 알람을 등록한다.
                firebase_response = await self.action_usecase.send_alarm(alarm_result)

                return firebase_response
            # 2-2 단계
            # elif action_type == "exercise_counter":
                # 3단계 카운트를 실행시킬 코드를 LLM한테서 받아옴.

                # 4단계 펑션콜 코드를 실행. 플러터에 던져줌

            # 3단계 펑션콜로, 파이썬이 '액션에 대한 내용'을 파이어베이스에 던진다. 리턴은 성공여부만
                # action_result = await handle_action_request(action_type, {"user_id": user_id, "question": question})
            


        else:
            return {"response": "에이전트의 역할에서 벗어나는 내용입니다."}
