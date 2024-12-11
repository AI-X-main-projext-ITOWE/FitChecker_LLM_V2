import json
from agent.action import action_usecase
from agent.gpt.history_by_user.memory.memory_manager import *
from agent.gpt.model.llm_models import *
from agent.gpt.classify.analyzer import *
from agent.gpt.history_by_user.conversation_manager import *
from util.env_manager import *



class GptUsecase:
    def __init__(self):
        self.openai_api_key = get_openai_api_key()
        self.model_name = "gpt-4o-mini"
        self.model, self.system_message = get_gpt_model(self.model_name, self.openai_api_key, 0.7, 1000)


    # 1단계 : advice or action 판단
    async def process_question(self, user_id: int, question: str) -> dict:
        system_message_str = self.system_message.content
        analyzed = await analyze(self.model, question, system_message_str)
        return analyzed

    async def request_action_llm(self, user_id: int, question: str, analyzed: dict) -> dict:
        if not analyzed.get("is_action_request"):
            return {"response": "액션 요청이 아닙니다."}

        action_type = analyzed.get("action_type")
        action_data = {"user_id": user_id, "question": question}
        return await action_usecase(action_type, action_data)

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

    async def call_with_function(self, question: str):
    # 비동기 함수 호출 및 응답
        response = await get_function_call_model(self.model_name, self.openai_api_key, question)
        print(f"call_with_function response: {response}")

        # Response에서 'choices'를 확인
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            # 첫 번째 choice를 선택
            choice = response.choices[0]

            # choice 내 message와 function_call 존재 여부 확인
            if hasattr(choice, 'message') and hasattr(choice.message, 'function_call'):
                function_call = choice.message.function_call

                # function_call 내 arguments 확인
                if hasattr(function_call, 'arguments'):
                    try:
                        # arguments JSON 파싱
                        json_response = json.loads(function_call.arguments)
                        print(f"Parsed JSON response: {json_response}")

                        # 함수 이름에 따라 처리
                        function_name = function_call.name
                        
                        if function_name == "create_alarm":
                            # 알람 데이터 처리
                            response = json_response.get('response', '답변이 지정되지 않았습니다.')
                            
                            alarm_time = json_response.get('alarm_time', '알람 시간이 지정되지 않았습니다.')
                            alarm_text = json_response.get('alarm_text', '알람 내용이 지정되지 않았습니다.')
                            print(f"알람 세부사항 - 시간: {alarm_time}, 내용: {alarm_text}")
                            return {'response' : response, 'alarm_time': alarm_time, 'alarm_text': alarm_text}

                        elif function_name == "create_counter":
                            # 카운터 데이터 처리
                            sets = json_response.get('sets', 0)
                            reps_per_set = json_response.get('reps_per_set', 0)
                            exercise = json_response.get('exercise', 'unknown')
                            print(f"카운터 세부사항 - 세트 수: {sets}, 반복 횟수: {reps_per_set}, 운동 이름: {exercise}")
                            return {'sets': sets, 'reps_per_set': reps_per_set, 'exercise': exercise}

                    except json.JSONDecodeError as e:
                        print(f"JSON 디코딩 오류: {e}")
                        return None
                else:
                    print("function_call에 arguments가 없습니다.")
                    return None
            else:
                print("function_call이 응답에 포함되어 있지 않습니다.")
                return None
        else:
            print("유효하지 않은 응답 또는 빈 choices.")
            return None
