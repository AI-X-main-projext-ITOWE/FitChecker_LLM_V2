from agent.rag.embedding.model.embedding_model import get_embedding_model

class EmbeddingOperator():
    def __init__(self) -> None:
        self.model = get_embedding_model()

    def execute(self, document:str):
        return self.model.encode(document)
    
    