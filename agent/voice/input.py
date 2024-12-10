import io
import wave
from fastapi import HTTPException
import speech_recognition as sr


class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()  # SpeechRecognition 라이브러리의 음성 인식기 초기화

    def process_audio_bytes(self, audio_bytes: bytes) -> str:
      
        try:
            # 1. WAV 포맷인지 확인
            try:
                with wave.open(io.BytesIO(audio_bytes), 'rb') as wav_file:
                    wav_file.getparams()  # WAV 파일의 메타데이터 확인
            except wave.Error:
                raise HTTPException(status_code=400, detail="Invalid WAV format.")  # WAV 포맷이 아니면 예외 발생

            # 2. 음성 데이터를 텍스트로 변환
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio_data = self.recognizer.record(source)  # 음성 데이터를 로드
            return self.recognizer.recognize_google(audio_data, language="ko-KR").strip()  # Google API로 텍스트 변환

        except wave.Error:
            raise HTTPException(status_code=400, detail="Invalid WAV format.")  # WAV 오류 처리
        except sr.UnknownValueError:
            raise HTTPException(status_code=400, detail="Speech could not be understood.")  # 음성 인식 실패 처리
        except sr.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Speech recognition service error: {e}")  # API 요청 오류 처리
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Audio processing error: {e}")  # 기타 오류 처리
