from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from llm.dto.request.recommend_request import *
from util.env_manager import *


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "LLM World"}

@app.get("/recommendation")
def requestMessage(request: RecommendRequest):
    title = request.title

    return {title}