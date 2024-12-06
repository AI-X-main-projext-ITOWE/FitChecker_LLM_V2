from langchain.memory import ConversationSummaryBufferMemory
from agent.gpt.model.llm_models import get_langchain_model, ChatOpenAI  # 필요한 경우 import하세요

# 사용자별 메모리 저장소
store = {}

def get_Memory_manager(user_id: int, llm: ChatOpenAI) -> ConversationSummaryBufferMemory:
    """
    사용자 ID에 해당하는 ConversationSummaryBufferMemory 반환.
    """
    if user_id in store:
        print(f"'{user_id}' 키가 존재합니다.")
        return store[user_id]
    else:
        print(f"'{user_id}' 키가 존재하지 않습니다. 새로운 메모리를 생성합니다.")
        # 새로운 메모리 생성 및 저장
        new_memory = get_langchain_model(llm, user_id)
        store[user_id] = new_memory
        return new_memory

def add_memory(user_id: int, memory: ConversationSummaryBufferMemory):
    store[user_id] = memory
