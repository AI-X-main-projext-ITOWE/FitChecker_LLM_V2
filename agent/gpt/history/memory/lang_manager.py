from gpt.history.conversation_manager import ConversationManager
from langchain.memory import ConversationSummaryBufferMemory

# 사용자별 메모리 저장소
store = {}

def get_conversation_manager(user_id: int) -> ConversationManager:
    """
    사용자 ID에 해당하는 ConversationManager 반환.
    :param user_id: 사용자 ID
    :return: ConversationManager 객체 또는 None
    """
    if user_id in store:
        print(f"'{user_id}' 키가 존재합니다.")
        return store[user_id]
    else:
        print(f"'{user_id}' 키가 존재하지 않습니다.")
        return None


def add_conversation_manager(user_id: int, memory: ConversationSummaryBufferMemory):
    store[user_id] = ConversationManager(memory)
