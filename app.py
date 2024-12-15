from fastapi import Body, FastAPI, File, Query, UploadFile
from fastapi import FastAPI
from agent.action.alarm.scheduler.setup.scheduler_setup import scheduler
from fastapi.middleware.cors import CORSMiddleware
from agent.action.alarm.init.firebase_init import *
from agent.agent_usecase import AgentUsecase
import uvicorn
from agent.dto.request.recommend_request import RecommendRequest
from agent.dto.request.recommend_request import *
from util.env_manager import *
from agent.rag.rag_usecase import *
import sys
import os



# 프로젝트 루트 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
initalize_firebase()
app = FastAPI()
agent_usecase = AgentUsecase()


# cors 설정 
cors_origins = get_cors_origins().split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # 여러 도메인을 허용
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 필요한 메서드만 허용
    allow_headers=["Content-Type", "Authorization"],  # 필요한 헤더만 허용
)



@app.post("/api/v1/agent")
async def agents(
    request: RecommendRequest = Body(None), input_type: str = Query(default="text"), audio_file: UploadFile = File(None)):

    audio_bytes = None
    if input_type == "voice" and audio_file:
        audio_bytes = await audio_file.read()

    response = await agent_usecase.execute(request, input_type, audio_bytes)
    return {"response": response}


@app.get("/api/v1/embbeding")
async def embbedings():
    rag = RagUsecase()
    result = rag.embedding_documents()

    return {"result": result}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)