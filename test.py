import asyncio
import requests
import speech_recognition as sr
import os
from agent.dto.request.recommend_request import RecommendRequest
from agent.voice.input import VoiceInput
from agent.agent_usecase import AgentUsecase

async def test_full_agent_logic_with_microphone():
    """
    마이크로 음성을 입력받아 Whisper API를 통해 텍스트로 변환한 후, AgentUsecase로 처리.
    """
    recognizer = sr.Recognizer()
    voice_input = VoiceInput()  # VoiceInput 클래스 인스턴스 생성
    agent_usecase = AgentUsecase()

    print("마이크로 실시간 음성을 입력하세요...")
    try:
        with sr.Microphone() as source:
            print("녹음 중입니다. 말을 시작하세요!")

            # 음성 데이터 녹음
            audio = recognizer.listen(source, timeout=5)
            print("녹음 완료. Whisper API를 통해 처리 중...")

            # 음성을 bytes 형태로 변환
            audio_bytes = audio.get_wav_data()

            # RecommendRequest 생성
            request = RecommendRequest(
                user_id="test_user",
                fcm_token="test_token",
                question=None,  # 음성 데이터를 텍스트로 변환 후 여기에 값이 들어감
                weight=70,
                height=175,
                gender="male",
                age=25,
            )

            # AgentUsecase 실행, 음성 데이터는 AgentUsecase 내에서 처리
            response = await agent_usecase.execute(
                request=request,
                input_type="voice",
                audio_bytes=audio_bytes
            )

            # FastAPI 서버 로직을 통합적으로 검증
            print(f"Agent 응답: {response}")

    except sr.WaitTimeoutError:
        print("녹음 시간이 초과되었습니다. 다시 시도하세요.")
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다. 다시 시도하세요.")
    except sr.RequestError as e:
        print(f"음성 인식 서비스에 문제가 발생했습니다: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Whisper API 요청 실패: {e}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    asyncio.run(test_full_agent_logic_with_microphone())
