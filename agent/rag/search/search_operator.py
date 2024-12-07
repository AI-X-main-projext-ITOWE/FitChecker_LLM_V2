from agent.rag.embedding_db.model.elasticsearch_creator import elastic_creator


class Elastic_Search():
    def __init__(self):
        self.es = elastic_creator

    def search_similar_vector(self, index_name, query_vector, top_k=5):
        response = self.es.search(
            index = index_name,
            query = {
                "script_sore" : {
                    "query" : {"match_all" : {}},
                    "script" : {
                        "source" : "cosineSimilarity(params.query_vector, 'vector') +1.0",
                        "params" : {"query_vector" : query_vector}
                    }
                }
            },
            size = top_k
        )
        return response["hits"]["hits"]
    
    