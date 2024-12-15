import requests
from fastapi import HTTPException
from util.env_manager import get_openai_api_key

class VoiceInput:
    def __init__(self):
        # OpenAI API 키 설정
        self.openai_api_key = get_openai_api_key()
        if not self.openai_api_key:
            raise ValueError("환경 변수 'OPENAI_API_KEY'가 설정되지 않았습니다.")

    def process_audio_file(self, audio_file_path: str) -> str:
        """
        음성 파일 경로를 받아 Whisper API를 사용해 텍스트로 변환.
        """
        try:
            # Whisper API URL 및 헤더 설정
            url = "https://api.openai.com/v1/audio/transcriptions"
            headers = {"Authorization": f"Bearer {self.openai_api_key}"}

            # 파일을 OpenAI Whisper API로 전송
            with open(audio_file_path, "rb") as audio_file:
                files = {
                    "file": (audio_file_path, audio_file, "audio/wav"),
                    "model": (None, "whisper-1"),
                }
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()

            # Whisper API 응답 처리
            transcript = response.json()
            if "text" in transcript and transcript["text"].strip():
                return transcript["text"].strip()
            else:
                raise HTTPException(status_code=500, detail="Failed to transcribe audio.")

        except requests.exceptions.RequestException as e:
            # HTTP 요청 오류 처리
            raise HTTPException(status_code=500, detail=f"Whisper API call failed: {e}")
        except Exception as e:
            # 일반적인 예외 처리
            raise HTTPException(status_code=500, detail=f"Audio processing error: {e}")
