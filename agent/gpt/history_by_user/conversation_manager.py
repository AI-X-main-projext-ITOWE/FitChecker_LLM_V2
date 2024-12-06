from langchain.memory import ConversationSummaryBufferMemory

class ConversationManager:
    def __init__(self, user_history_langchain: ConversationSummaryBufferMemory):
        self.memory = user_history_langchain
        
    async def add_message(self, user_message: str, ai_message: str) -> str:
        """
        사용자 입력 메시지를 추가하고 AI 응답을 저장 (비동기 메서드)
        """
        await self.memory.save_context({"input": user_message}, {"output": ai_message})
        return ai_message
    
    async def get_chat_history(self):
        """
        대화 기록 반환 (비동기 메서드)
        """
        return await self.memory.load_memory_variables({})

    async def clear_memory(self):
        """
        대화 메모리 초기화 (비동기 메서드)
        """
        await self.memory.clear()

    def get_memory(self):
        return self.memory
