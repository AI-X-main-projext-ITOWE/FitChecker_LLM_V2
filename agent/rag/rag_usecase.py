from agent.rag.chunking.chunk_operator import *
from agent.rag.embedding.embedding_operater import *
from agent.rag.util.file_loader_util import * 
from util.env_manager import *
import os


class RagUsecase():

    def __init__(self):
        self.chunk_operator = ChunkOperator()
        self.embedding_operator = EmbeddingOperator()
        

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


      
    
       

        

