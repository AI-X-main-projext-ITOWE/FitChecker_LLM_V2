from elasticsearch import Elasticsearch
from util.env_manager import *
from agent.rag.embedding_db.model.elasticsearch_creator import *

host = get_elasticsearch_url

class ElasticVectorDB():
    def __init__(self):
        self.es = elastic_creator()

    def create_index(self, index_name):
        """
        es_client : Elasticsearch 클라이언트 객체
        index_name : 생성할 인덱스 이름
        vector_dim : dense_vector 차원수
        """
        mapping = {
            "mappings" : {
                "properties" : {
                    "vector" : {
                        "type" : "dense_vector",
                        "dims" : 1024
                    },
                    "text": {
                        "type" : "text"
                    }
                }
            }
        }
    
        # 인덱스가 없으면 생성
        if not self.es.indices.exists(index=index_name):
            response = self.es.indices.create(index=index_name, body=mapping)
            print(f"인덱스 '{index_name}' 생성 완료")
            return response
        else:   
            print(f"인덱스 '{index_name}'는 이미 존재합니다")
            return None
        
    def store_vector(self, index_name, embeddings, text):
        """Elasticsearch에 벡터 데이터를 저장하는 메서드
        index_name : 데이터를 저장할 인덱스 이름
        embeddings : 벡터 데이터 리스트
        return : 저장된 데이터 개수
        i : 청킹 하나당의 인덱스
        """
        for i, (vector, text) in enumerate(zip(embeddings, text)):
            document = {'vector' : vector,
                        'text' : text
                        }
            self.es.index(index=index_name, id=i, document=document)

    def fetch_vector(self, index_name, size=1000):
        response = self.es.search(
            index=index_name,
            query={"match_all" : {}},
            size=size
        )
        vectors = [
            {
                "index" : hit["_index"], #문서가 포함된 인덱스 이름
                "id" : hit["_id"], #문서 아이디 
                "vector" : hit["_source"]["vector"], #저장된 벡터값
                "text" : hit["_source"]["text"]
            }
            for hit in response["hits"]["hits"]
        ]
        return vectors