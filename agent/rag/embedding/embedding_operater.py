from agent.rag.embedding.model.embedding_model import get_embedding_model
import numpy as np
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
from util.env_manager import *



# 평균 풀링 함수
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

class EmbeddingOperator():
    def __init__(self) -> None:
        model_name = get_embedding_model()
        token = get_huggingface_token()
        # 모델 및 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
        self.model = AutoModel.from_pretrained(model_name, use_auth_token=token)

    def execute(self, document: str):
        # 입력 텍스트 전처리 (E5 모델 형식: "query: " 또는 "passage: ")
        # processed_text = f"query: {document}"  # 텍스트에 접두어 추가
        
        # 텍스트 토크나이즈
        batch_dict = self.tokenizer(
            document, max_length=512, padding=True, truncation=True, return_tensors='pt'
        )
        
        # 모델에 입력하여 임베딩 생성
        outputs = self.model(**batch_dict)
        embedding = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        
        # 벡터 정규화 (L2 정규화)
        normalized_embedding = F.normalize(embedding, p=2, dim=1).detach().cpu().numpy()
        
        # numpy 배열을 리스트로 변환
        if isinstance(normalized_embedding, np.ndarray):
            normalized_embedding = normalized_embedding.tolist()
        
        return normalized_embedding[0]  # 1차원 벡터 반환
        

    def Reverse_embedding(self, results):
        # 결과에서 점수와 텍스트를 추출
        extracted_texts = [
            {
                "score": result["_score"],
                "text": result["_source"]["text"],
            }
            for result in results
        ]
        return extracted_texts
