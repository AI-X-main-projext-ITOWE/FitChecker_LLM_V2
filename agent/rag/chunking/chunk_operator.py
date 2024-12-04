from agent.rag.chunking.model.chunk_model import get_text_splitter



class ChunkOperator():

    def __init__(self):
        self.chunk_model = get_text_splitter()
        

    def text_spliter(self, extracted_text):
        chunks = self.chunk_model.split_text(extracted_text)

        return chunks

