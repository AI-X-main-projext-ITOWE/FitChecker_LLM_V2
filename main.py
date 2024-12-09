import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from agent.agent_usecase import AgentUsecase
import uvicorn
from agent.dto.request.recommend_request import RecommendRequest

app = FastAPI()
agent_usecase = AgentUsecase()


@app.post("/api/v1/agent")
async def agents(request: RecommendRequest):
    response = await agent_usecase.execute(request)  # await 필수
    return {"response": response}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
