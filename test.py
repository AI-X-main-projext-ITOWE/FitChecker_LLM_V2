import asyncio
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
            audio = recognizer.listen(source, timeout=5)  # 5초 대기
            print("녹음 완료. Whisper API로 전송 중...")

            # 음성을 WAV 파일로 저장
            audio_path = "temp_audio.wav"
            with open(audio_path, "wb") as f:
                f.write(audio.get_wav_data())

            # VoiceInput을 사용하여 텍스트 변환
            question = voice_input.process_audio_file(audio_path)
            print(f"변환된 텍스트: {question}")

            # 임시 파일 삭제
            os.remove(audio_path)


            request = RecommendRequest(
                user_id="test_user",
                fcm_token="test_token",
                question=question,
                weight=70,
                height=175,
                gender="male",
                age=25
            )

            response = await agent_usecase.execute(request=request, input_type="text")
            print(f"Agent 응답: {response}")
            
            # AgentUsecase 호출
            response = await agent_usecase.execute(
                request=None,  # 음성 입력만 사용하는 경우 RecommendRequest는 없음
                input_type="text",  # 텍스트로 변환된 결과를 사용
                audio_bytes=None
            )

            print(f"Agent 응답: {response}")

    except sr.WaitTimeoutError:
        print("녹음 시간이 초과되었습니다. 다시 시도하세요.")
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다. 다시 시도하세요.")
    except sr.RequestError as e:
        print(f"음성 인식 서비스에 문제가 발생했습니다: {e}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    asyncio.run(test_full_agent_logic_with_microphone())
