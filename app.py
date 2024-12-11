from fastapi import Body, FastAPI, Query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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



app = FastAPI()
agent_usecase = AgentUsecase()


# cors 설정 
cors_origins = get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origins],  # 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 필요한 메서드만 허용
    allow_headers=["Content-Type", "Authorization"],  # 필요한 헤더만 허용
)



@app.post("/api/v1/agent")
async def agents(request: RecommendRequest, input_type: str = Query(default="text"), audio_bytes: bytes = Body(None)):
    response = await agent_usecase.execute(request, input_type, audio_bytes)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# @app.get("/")
# def read_root():
#     return {"Hello": "LLM World"}

# @app.post("/recommendation")
# def requestMessage(request: RecommendRequest):
#     title = request.title
#     return {title}

# @app.get("/ragtest_pdf_embedding")
# async def requestMessage():
#     rag_usecase = RagUsecase()
#     vector = rag_usecase.embedding_documents()
    
#     return {"vector" : vector}

# @app.post("/ragtest_query_embedding")
# def requestMessage(request: RecommendRequest):
#     text = request.question
#     rag_usecase = RagUsecase()
#     embeddings = rag_usecase.embedding_query(text)

#     return {"embeddings" : embeddings}

# @app.post("/ragtest_extract_similarity")
# def requestMessage(request : RecommendRequest):
#     text = request.question
#     rag_usecase = RagUsecase()
#     results = rag_usecase.extract_similarity(text)

#     return results

# @app.post("/ragtest_extract_text")
# def requestMessage(request : RecommendRequest):
#     text = request.question
#     rag_usecase = RagUsecase()
#     extract_text = rag_usecase.extract_text(text)

#     return {"results" : extract_text}