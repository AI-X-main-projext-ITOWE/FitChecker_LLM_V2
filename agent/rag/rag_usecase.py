from agent.rag.chunking.chunk_operator import *
from agent.rag.embedding.embedding_operater import *
from agent.rag.util.file_loader_util import * 
from util.env_manager import *
import os
from agent.rag.embedding_db.elasticsearch_embedding import *
from agent.rag.search.search_operator import Elastic_Search
from agent.dto.request.recommend_request import RecommendRequest

class RagUsecase():

    def __init__(self):
        self.chunk_operator = ChunkOperator()
        self.embedding_operator = EmbeddingOperator()
        self.elasticvector_db = ElasticVectorDB()
        self.elastic_search = Elastic_Search()
        self.index_name = "embeddings_index"

    def embedding_documents(self):
        #  1. 문서를 가져온다.
        pdf_file_path = get_pdf_folder_path()
          #  2. 문서를 텍스트로 추출한다.
        pdf_sentence = extract_pdf_sentence(pdf_file_path)
        #  3. 텍스트를 청킹한다.
        chunks = self.chunk_operator.text_spliter(pdf_sentence)
       
         #  4. 청킹된 데이터를 벡터임베딩한다.
        embeddings = []
        for chunk in chunks:
            embeddings.append(self.embedding_operator.execute(chunk))
        #  5. 디비에 저장.
            #5-1. 인덱스 생성 (문서 카테고리. 식단과 운동스케줄 등)
        
        vector_dim = 768
        self.elasticvector_db.create_index(index_name = self.index_name, vector_dims = vector_dim)
        #5-2. 벡터 데이터 저장
        self.elasticvector_db.store_vector(index_name = self.index_name, embeddings = embeddings)
                
    def embedding_query(self, question:str):
        #1. 사용자 입력 쿼리를 가져와 청킹한다
        chunks = self.chunk_operator.text_spliter(question)
        #2. 청킹된 입력 쿼리를 벡터임베딩화 한다.
        embeddings = []
        for chunk in chunks:
            embeddings.append(self.embedding_operator.execute(chunk))

        return embeddings
        
    #4. 사용자 입력 쿼리와 저장된 데이터에서의 유사한 벡터 검색
    def extract_similarity(self, question : str):      
        #1. 사용자 입력쿼리 가져오기
        embeddings = self.embedding_query(question)
        #3. 유사도계산
        self.elastic_search.search_similar_vector(query_vector=embeddings, index_name = self.index_name, top_k=5)
            