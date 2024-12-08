import requests
from agent.voice.input import VoiceInput

# FastAPI 서버 URL
FASTAPI_URL = "http://127.0.0.1:8000/api/v1/agent"

def test_real_time_voice():
    voice_input = VoiceInput()
    print("마이크로 음성을 입력하세요...")

    # 음성 입력 받기
    question = voice_input.listen()
    if not question:
        print("음성을 인식하지 못했습니다. 다시 시도해주세요.")
        return

    print(f"Recognized question: {question}")

    # FastAPI에 POST 요청
    data = {
        "user_id": 1,
        "question": question
    }
    response = requests.post(FASTAPI_URL, params={"input_type": "voice"}, json=data)

    # FastAPI 응답 출력
    print(f"API Response: {response.json()}")

# 테스트 실행
if __name__ == "__main__":
    test_real_time_voice()
