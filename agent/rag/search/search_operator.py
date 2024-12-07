from agent.rag.embedding_db.model.elasticsearch_creator import elastic_creator


class Elastic_Search():
    def __init__(self):
        self.es = elastic_creator()

    def search_similar_vector(self, index_name, query_vector, top_k):
        try:
            response = self.es.search(
                index=index_name,
                body={
                    "size": top_k,
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": """
                                    double cosineSim = cosineSimilarity(params.query_vector, 'vector');
                                    return Math.max(0, cosineSim);
                                """,
                                "params": {
                                    "query_vector": query_vector[0]
                                }
                            }
                        }
                    }
                }
            )
            return response["hits"]["hits"]
        except Exception as e:
            # print(f"Error during Elasticsearch query: {e}")
            # print(f"Query vector: {query_vector}")
            raise
    