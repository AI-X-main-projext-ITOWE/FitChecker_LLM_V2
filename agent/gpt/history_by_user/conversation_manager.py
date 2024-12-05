from langchain.memory import ConversationSummaryBufferMemory


class ConversationManager:
    def __init__(self, user_history_langchain: ConversationSummaryBufferMemory):
        """
        대화 관리를 위한 클래스 초기화
        :param llm: LangChain의 LLM 객체
        :param max_token_limit: 요약할 토큰의 최대 한도
        """
        self.memory = user_history_langchain
        
    def add_message(self, user_message: str, ai_message: str) -> str:
        """
        사용자 입력 메시지를 추가하고 AI 응답을 생성
        :param input_message: 사용자의 대화 입력
        :return: AI 응답
        """
        self.memory.save_context({"input": user_message}, {"output": ai_message})
        return ai_message
    
    def get_chat_history(self):
        """
        대화 기록 반환
        :return: 현재까지 저장된 대화 내용
        """
        return self.memory.load_memory_variables({})

    def clear_memory(self):
        """
        대화 메모리 초기화
        """
        self.memory.clear()

    def get_memory(self):
        return self.memory