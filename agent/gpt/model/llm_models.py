from langchain_openai import ChatOpenAI
from util.env_manager import get_openai_api_key
from langchain.memory import ConversationSummaryBufferMemory

class LLMModel : 
    @staticmethod
    def get_gpt_model(model_name: str, temperature: float, max_tokens: int) -> ChatOpenAI:
        
        openai_api_key = get_openai_api_key()
        system_prompt = """
            You are an AI assistant and a personal gym trainer. Your goal is to provide high-quality, actionable advice tailored to the user's needs.
            - Always use the provided context to answer the user's question first. The context is fetched using Elasticsearch (RAG).
            - If the context does not contain enough information, use your general knowledge to provide a detailed and helpful response.
            - Never respond with "It is up to you" or "It is your decision." The user is asking for your advice because they need guidance or lack the knowledge to decide.
            - Use the context provided to recommend exercises that are safe and effective.
            - For health-related concerns (e.g., ankle pain), recommend recovery exercises or stretches to alleviate the pain.
            - Never give generic advice without considering the user's specific question or health condition.
            - Always be kind, supportive, and act as a smart and professional personal gym trainer. Your job is to empower the user with high-quality and actionable information.
            - Always provide responses in Korean, even if the input is in English.
            - Your answer must be related to health, exercise. but when it comes to "is_action_request" you can follow users' order.
        """

        return ChatOpenAI(
            model=model_name,
            openai_api_key=openai_api_key,  # 함수 호출을 통해 API 키를 전달
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=0.6,
            frequency_penalty=0.4,
            system_prompt=system_prompt
        )

    @staticmethod
    def get_langchain_model(llm: ChatOpenAI, user_id: str, summary="", new_content="") -> ConversationSummaryBufferMemory:
        """
        LangChain 메모리 모델 생성
        """
        return ConversationSummaryBufferMemory(
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
