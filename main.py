from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException
from agent.dto.request.recommend_request import *
from agent.dto.request.test_request import TestRequest
from agent.gpt import gpt_operator
from agent.gpt.gpt_operator import GptOperator
from util.env_manager import *
import uvicorn


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "LLM World"}

@app.get("/recommendation")
def requestMessage(request: RecommendRequest):
    title = request.title


@app.post("/analizetest")
async def request_message(request: TestRequest):
    user_id = request.user_id
    question = request.question

    gpt_usecase = GptOperator()

    analyzed_result = await gpt_usecase.process_question(user_id, question)
    return {
        "user_id": user_id,
        "question": question,
        "analysis": analyzed_result,
    }

@app.post("/gpttest")
async def gpt_test(request: TestRequest):
    gpt_usecase = GptOperator()

    try:
        result = await gpt_usecase.request_advice_llm(
            user_id=request.user_id,
            question=request.question,
            rag_context=request.ragtext
        )
        return {"user_id": request.user_id, "question": request.question, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)