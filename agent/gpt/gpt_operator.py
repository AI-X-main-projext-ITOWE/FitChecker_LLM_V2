from agent.gpt.model.llm_models import *
from agent.gpt.classify.analyzer import *
from agent.gpt.model.llm_models import LLMModel



class GptOperator():
    def __init__(self):
        openai_api_key = get_openai_api_key()

        self.model = LLMModel.get_gpt_model("gpt-4o-mini",openai_api_key, 0.7, 1000)

        self.llm_OG = LLMModel()

    async def process_question(self, question: str):
        analyzed = await analyze(self.model, question)

        return analyzed
