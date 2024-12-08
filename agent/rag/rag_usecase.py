# 모듈 임포트
from agent.rag.search.search_operator import Elastic_Search
from agent.rag.embedding_db.elasticsearch_embedding import *
from agent.rag.chunking.chunk_operator import *
from agent.rag.embedding.embedding_operater import *
from agent.rag.util.file_loader_util import * 
from agent.rag.util.data_preprocessor_util import *
from util.env_manager import *

# 루트 디렉토리 경로 추가

class RagUsecase():

    def __init__(self):
        self.chunk_operator = ChunkOperator()
        self.embedding_operator = EmbeddingOperator()
        self.elasticvector_db = ElasticVectorDB()
        self.elastic_search = Elastic_Search()
        self.index_name = "embeddings_index8"

    #5. 역임베딩 (임베딩화 할 때 추가로 저장한 텍스트 추출)
    def extract_text(self, question : str):
        results = self.extract_similarity(question)
        text = self.embedding_operator.Reverse_embedding(results)
        #6. 데이터 전처리
        cleaned_text = preprocess_results(text)
        return cleaned_text
    
    
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
        self.elasticvector_db.create_index(index_name = self.index_name)
        #5-2. 벡터 데이터 저장
        self.elasticvector_db.store_vector(index_name = self.index_name, embeddings = embeddings, text = chunks)
        
        vectors = self.elasticvector_db.fetch_vector(index_name = self.index_name)
        
        return vectors
                
    def embedding_query(self, question:str):
        #1. 사용자 입력 쿼리를 가져와 청킹한다
        chunks = self.chunk_operator.text_spliter(question)
        #2. 청킹된 입력 쿼리를 벡터임베딩화 한다.
        embeddings = []
        for chunk in chunks:
            embedding = self.embedding_operator.execute(chunk)
            embeddings.append(embedding)

        return embeddings
        
    #4. 사용자 입력 쿼리와 저장된 데이터에서의 유사한 벡터 검색
    def extract_similarity(self, question : str):      
        #1. 사용자 입력쿼리 가져오기
        embeddings = self.embedding_query(question)
        #3. 유사도계산
        index_name=self.index_name,
        query_vector=embeddings
        top_k=5
        results = self.elastic_search.search_similar_vector(query_vector=query_vector, index_name = index_name, top_k=top_k)
    
        # print(f"Search results: {results}")

        return results    

    
    
