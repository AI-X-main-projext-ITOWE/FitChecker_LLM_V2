import requests
from fastapi import HTTPException
from util.env_manager import get_openai_api_key

class VoiceInput:
    def __init__(self):
        # OpenAI API 키 설정
        self.openai_api_key = get_openai_api_key()
        if not self.openai_api_key:
            raise ValueError("환경 변수 'OPENAI_API_KEY'가 설정되지 않았습니다.")

    def process_audio(self, audio: bytes) -> str:
        """
        음성 데이터를 bytes로 받아 Whisper API를 사용해 텍스트로 변환.
        """
        if not audio:
            raise ValueError("Audio data is required.")

        try:
            # Whisper API 호출
            url = "https://api.openai.com/v1/audio/transcriptions"
            headers = {"Authorization": f"Bearer {self.openai_api_key}"}
            files = {
                "file": ("audio.wav", audio, "audio/wav"),
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
            raise HTTPException(status_code=500, detail=f"Whisper API call failed: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Audio processing error: {e}")
