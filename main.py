import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from agent.agent_usecase import AgentUsecase
from agent.dto.request.recommend_request import RecommendRequest
import uvicorn
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 초기화
app = FastAPI()

# Usecase 인스턴스 생성
agent_usecase = AgentUsecase()

# 엔드포인트 정의
@app.post("/api/v1/agent")
async def agents(request: RecommendRequest, input_type: str = Query(default="text")):
    response = await agent_usecase.execute(request, input_type="")
    logger.info(f"Generated response: {response}")
    return {"response": response}

# 애플리케이션 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
