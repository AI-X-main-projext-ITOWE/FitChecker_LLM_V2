import sys
import os

from agent.dto.response.advice.advice_response import AdviceResponse
from agent.dto.response.recommend_response import RecommendResponse

# 현재 파일 위치를 기준으로 프로젝트 루트 경로를 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.dto.request.recommend_request import RecommendRequest
from agent.voice.input import *
from .rag.rag_usecase import RagUsecase
from .gpt.gpt_usecase import GptUsecase
from .action.action_usecase import*
from .gpt.gpt_usecase import GptUsecase
from .dto.request.recommend_request import RecommendRequest
from .action.action_usecase import *
from .action.alarm.firebase_request import *

class AgentUsecase:
    def __init__(self):
        self.gpt_usecase = GptUsecase()
        self.rag_usecase = RagUsecase()
        self.voice_input = VoiceInput()
        self.action_usecase = ActionUsecase()

    async def execute(self, request: RecommendRequest = None, input_type: str = "text", audio_bytes: bytes = None) -> RecommendResponse:
        """
        요청의 타입에 따라 동작을 처리하는 메인 함수.
        """
        # RecommendRequest 객체 처리
        if request:
            user_id = request.user_id
            question = f"{request.question}"
        else:
            user_id = None
            question = None

        # 음성 입력 처리
        if input_type == "voice" and audio_bytes:
            question = self.voice_input.process_audio_bytes(audio_bytes)
        elif input_type == "text" and not question:
            return {"response": "Text input is empty."}

        # GPT 분석 요청
        action_or_advice = await self.gpt_usecase.process_question(user_id, question)

        if action_or_advice.get("is_advice_request"):
            recommend_response = RecommendResponse()
            advice = AdviceResponse()
            
            # 조언 생성 로직
            rag_result = self.rag_usecase.extract_text(question)
            gpt_result_advice = await self.gpt_usecase.request_advice_llm(user_id, question, rag_result)

            # 어드바이스 리스폰스에 값을 담는다
            advice.response = gpt_result_advice
            # 리커맨드 리스폰스에 어드바이스 리스폰스를 담아서 플러터에 전달
            recommend_response.advice_response = advice

            return recommend_response

        elif action_or_advice.get("is_action_request"):
            action_type = action_or_advice.get("action_type")
            action_data = action_or_advice.get("action_data", {})

             # 2단계 액션 타입을 분리함
            # 2-1단계
            if action_type == "alarm":
                

                # 3단계 LLM한테 펑션콜 코드를 받아옴.
                alarm_result = await self.gpt_usecase.call_with_function(question)
                # 4단계 펑션콜 코드를 실행해서 파이어베이스에 알람을 등록한다.
                firebase_response = await self.action_usecase.send_alarm(alarm_result)

                return firebase_response
            # 특정 액션 실행
            elif action_type == "exercise_counter":
                

                exercise_counter_result = await self.gpt_usecase.call_with_function(question)
                exercise_counter_response  = await self.action_usecase.send_exercise_counter(exercise_counter_result)

                return exercise_counter_response 

        return {"response": "Unable to determine the request type."}
