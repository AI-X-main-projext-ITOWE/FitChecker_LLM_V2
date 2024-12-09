from langchain_openai import ChatOpenAI
from util.env_manager import *
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import SystemMessage


def get_gpt_model(model_name: str, openai_api_key: str, temperature: float, max_tokens: int) -> tuple[ChatOpenAI, SystemMessage]:
    """
    GPT 모델 생성
    """
    # 시스템 프롬프트를 호출 시 사용하기 위한 시스템 메시지로 정의
    system_message = SystemMessage(
        content=(
            "You are an AI assistant and a personal gym trainer. Your goal is to provide high-quality, actionable advice tailored to the user's needs.\n"
            "- Always use the provided context to answer the user's question first. The context is fetched using Elasticsearch (RAG).\n"
            "- If the context does not contain enough information, use your general knowledge to provide a detailed and helpful response.\n"
            "- Never respond with 'It is up to you' or 'It is your decision.' The user is asking for your advice because they need guidance or lack the knowledge to decide.\n"
            "- Use the context provided to recommend exercises that are safe and effective.\n"
            "- For health-related concerns (e.g., ankle pain), recommend recovery exercises or stretches to alleviate the pain.\n"
            "- Never give generic advice without considering the user's specific question or health condition.\n"
            "- Always be kind, supportive, and act as a smart and professional personal gym trainer. Your job is to empower the user with high-quality and actionable information.\n"
            "- Always provide responses in Korean, even if the input is in English.\n"
        )
    )

    # ChatOpenAI 모델을 생성
    return ChatOpenAI(
        model=model_name,
        openai_api_key=openai_api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        presence_penalty=0.6,
        frequency_penalty=0.4
    ), system_message


def get_langchain_model(llm: ChatOpenAI, user_id: int, summary="", new_content="") -> ConversationSummaryBufferMemory:
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        return_messages=True,
        memory_key=f"chat_history{user_id}",
        input_key="question",
        human_prefix="Human",
        ai_prefix="AI",
        summary_template=(
            "다음 요약을 사용해 대화의 핵심 내용을 정리하고 추적하세요:\n"
            f"대화 요약:\n{summary}\n"
            f"새로운 대화:\n{new_content}"
        )
    )
    print(f"LangChain Memory Initialized: {memory}")
    return memory
