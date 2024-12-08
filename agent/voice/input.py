import speech_recognition as sr
import logging

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self, default_text="기본 질문으로 진행합니다.") -> str:
        """
        Listen to the user's voice and return as a string.
        If no input is detected, return the default text.
        """
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise

            try:
                # Capture audio with timeout and phrase time limit
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio, language="ko-KR").strip()

                # Return the recognized text
                if not text:
                    logging.warning("No recognizable speech detected. Returning default text.")
                    return default_text

                logging.info(f"Recognized Text: {text}")
                return text

            except sr.WaitTimeoutError:
                logging.warning("Timeout reached. No audio input detected.")
                return default_text

            except sr.UnknownValueError:
                logging.error("Speech not understood.")
                return "음성을 이해할 수 없습니다. 다시 시도해주세요."

            except sr.RequestError as e:
                logging.error(f"STT service error: {e}")
                return "Google STT 서비스에 문제가 발생했습니다. 다시 시도해주세요."
