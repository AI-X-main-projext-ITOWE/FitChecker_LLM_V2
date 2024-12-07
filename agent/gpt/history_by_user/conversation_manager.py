from langchain.memory import ConversationSummaryBufferMemory

class ConversationManager:
    def __init__(self, user_history_langchain: ConversationSummaryBufferMemory):
        self.memory = user_history_langchain

    def add_message(self, user_message: str, ai_message: str) -> str:
        self.memory.save_context(
            {"question": user_message},
            {"response": ai_message}
        )
        return ai_message

    def get_chat_history(self) -> list:
        return self.memory.load_memory_variables({}).get(self.memory.memory_key, [])

    def get_summary(self) -> str:
        return self.memory.chat_memory.messages

    async def clear_memory(self):
        await self.memory.clear()

    def get_memory(self):
        return self.memory
