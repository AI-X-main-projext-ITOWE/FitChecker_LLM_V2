import sys
import os
from agent.dto.response.advice.advice_response import AdviceResponse
from agent.dto.response.alarm.alarm_response import AlarmResponse
from agent.dto.response.counter.counter_response import CounterResponse
from agent.dto.response.recommend_response import RecommendResponse

# 현재 파일 위치를 기준으로 프로젝트 루트 경로를 추가
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.dto.request.recommend_request import RecommendRequest
from agent.voice.input import *
from .rag.rag_usecase import RagUsecase
from .gpt.gpt_usecase import GptUsecase
from .action.action_usecase import*
from .gpt.gpt_usecase import GptUsecase
from .dto.request.recommend_request import RecommendRequest
from .action.action_usecase import *
from .action.alarm.alarm_usecase import *

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
            fcm_token = request.fcm_token
            question = f"질문: {request.question}, 체중: {request.weight}kg, 키: {request.height}cm, 성별: {request.gender}, 나이: {request.age}"
        else:
            user_id = None
            question = None

        # 음성 입력 처리
        if input_type == "voice" and audio_bytes:
            question = self.voice_input.process_audio_bytes(audio_bytes)
        elif input_type == "text" and not question:
            return RecommendResponse(
                advice_response=AdviceResponse(response="Text input is empty.")
            )

        # GPT 분석 요청
        action_or_advice = await self.gpt_usecase.process_question(user_id, question)

        # 초기화된 RecommendResponse 객체
        recommend_response = RecommendResponse()
        print(f"액션이냐 어드바이스냐 ?????? {action_or_advice}")
        if action_or_advice.get("is_advice_request"):
            advice = AdviceResponse()
            
            # 조언 생성 로직
            rag_result = self.rag_usecase.extract_text(question)
            gpt_result_advice = await self.gpt_usecase.request_advice_llm(user_id, question, rag_result)

            # 어드바이스 리스폰스에 값을 담는다
            advice.user_id = user_id
            advice.response = gpt_result_advice
            # 리커맨드 리스폰스에 어드바이스 리스폰스를 담아서 플러터에 전달
            recommend_response.advice_response = advice

            return recommend_response

        elif action_or_advice.get("is_action_request"):
            action_type = action_or_advice.get("action_type")
            alarm = AlarmResponse()

            # 액션 타입에 따른 처리
            if action_type == "alarm":
    
                # 3단계 LLM한테 펑션콜 코드를 받아옴.
                alarm_result = await self.gpt_usecase.call_with_function(question)
                # 4단계 펑션콜 코드를 실행해서 파이어베이스에 알람을 등록한다.
                firebase_response = await self.action_usecase.send_alarm(user_id, alarm_result, fcm_token)

                alarm.user_id = user_id
                alarm.alarm_id = firebase_response['name']
                alarm.alarm_time = alarm_result['alarm_time']
                alarm.alarm_text = alarm_result['alarm_text']
                alarm.response = alarm_result['response']

                recommend_response.alarm_response = alarm

                return recommend_response
            # 특정 액션 실행
            elif action_type == "exercise_counter":
                # GPT 결과에서 운동 관련 정보 추출
                exercise_counter_result = await self.gpt_usecase.call_with_function(question)

                # ActionUsecase 호출 및 데이터 검증
                exercise_counter_list = self.action_usecase.send_exercise_counter(exercise_counter_result)
            
                # CounterResponse에 결과 저장
                recommend_response.counter_response = CounterResponse(
                    user_id=user_id,
                    exercise=exercise_counter_list[0],
                    exercise_set=exercise_counter_list[1],
                    exercise_counter=exercise_counter_list[2],
                    response="운동 카운터 처리 완료"
                )

                return recommend_response
            # 요청 타입을 결정할 수 없는 경우 기본 응답 반환
        recommend_response.advice_response.response = "Unable to determine the request type."
        return recommend_response