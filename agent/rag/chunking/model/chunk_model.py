from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text_splitter():
    return RecursiveCharacterTextSplitter(
            chunk_size=500,  # 청크의 최대 크기
            chunk_overlap=50,  # 청크 간 겹치는 부분
            separators=["\n\n", "\n", ".", " "]  # 문단, 문장, 단어 단위로 분리
        )
