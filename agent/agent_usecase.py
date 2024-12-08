import sys
import os

# 현재 파일 위치를 기준으로 프로젝트 루트 경로를 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.voice.input import*
from .rag.rag_usecase import RagUsecase
from .gpt.gpt_operator import GptOperator
from .dto.request.recommend_request import RecommendRequest
from .action.handle_action_type import *
import logging
# {
#         "is_action_request": is_action_request,
#         "is_advice_request": is_advice_request,
#         "action_type": action_type,
#     }
class AgentUsecase:
    def __init__(self):
        self.gpt_usecase = GptOperator()
        self.rag_usecase = RagUsecase()
        self.voice_input = VoiceInput()

    async def execute(self, request: RecommendRequest, input_type: str = "text"):
        """
        요청을 처리하며, 입력 형태(텍스트 또는 음성)를 구분.
        """
        user_id = request.user_id
        question = request.question

        if input_type == "voice":
            question = self.voice_input.listen()
            if not question.strip():
                return {"response": "음성 입력을 인식하지 못했습니다. 다시 시도해주세요."}
            
        # 1단계: 비동기 호출
        action_or_advice = await self.gpt_usecase.process_question(user_id, question)

        if action_or_advice.get("is_advice_request"):
            # 2단계: RAG 결과 가져오기 (필요시 처리)
            rag_result = ""  # RAG 처리 로직 추가 필요
            # 3단계: LLM을 사용하여 조언 생성
            gpt_result_advice = await self.gpt_usecase.request_advice_llm(user_id, question, rag_result)
            return {"type": "advice", "result": gpt_result_advice}

        elif action_or_advice.get("is_action_request"):
            # 액션 수행
            action_type = action_or_advice.get("action_type")
            action_data = action_or_advice.get("action_data", {})
            gpt_result_action = await self.gpt_usecase.request_action_llm(user_id, question, action_type, action_data)
            return {"type": "action", "result": gpt_result_action}

        else:
            logging.warning("Unrecognized request type.")
            return {"response": "에이전트의 역할에서 벗어나는 내용입니다."}